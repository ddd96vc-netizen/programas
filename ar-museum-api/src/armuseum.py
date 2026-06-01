import cv2
import numpy as np
import sys
import os

# ─── Parámetros configurables ────────────────────────────────────────────────
MIN_MATCHES_FOR_HOMOGRAPHY = 25   # mínimo de matches para calcular homografía
RANSAC_REPROJ_THRESHOLD    = 5.0  # umbral de reproyección RANSAC (píxeles)
ORB_HAMMING_THRESHOLD      = 50   # umbral fijo Hamming para ORB
SIFT_RATIO_TEST            = 0.75 # ratio test de Lowe para SIFT
SMOOTHING_ALPHA            = 0.85 # factor de suavizado exponencial
MAX_BAD_FRAMES             = 5    # frames malos consecutivos antes de resetear
REPROJ_ERROR_THRESHOLD     = 10.0 # umbral de error de reproyección (píxeles)
DET_MIN                    = 0.001 # determinante mínimo de homografía válida


# ─── Funciones auxiliares ─────────────────────────────────────────────────────

def smooth_matrix(M_prev, M_new, alpha=SMOOTHING_ALPHA):
    """Suavizado exponencial entre dos homografías."""
    if M_prev is None:
        return M_new
    return alpha * M_prev + (1 - alpha) * M_new


def is_valid_homography(M):
    """Comprueba que M no contenga NaN/Inf y que su determinante sea razonable."""
    if M is None:
        return False
    if np.any(np.isnan(M)) or np.any(np.isinf(M)):
        return False
    if abs(np.linalg.det(M)) < DET_MIN:
        return False
    return True


def reprojection_error(src_pts, dst_pts, M):
    """Error medio de reproyección en píxeles."""
    projected = cv2.perspectiveTransform(src_pts, M)
    errors = np.linalg.norm(projected - dst_pts, axis=2)
    return float(np.mean(errors))


def load_model_descriptors(img_model):
    """Calcula keypoints y descriptores ORB y SIFT del modelo."""
    orb  = cv2.ORB_create(nfeatures=4000)
    sift = cv2.SIFT_create()
    kp_o, des_o = orb.detectAndCompute(img_model, None)
    kp_s, des_s = sift.detectAndCompute(img_model, None)
    return orb, sift, kp_o, des_o, kp_s, des_s


def match_features(orb, sift, bf_orb, bf_sift,
                   kp_m_o, des_m_o, kp_m_s, des_m_s,
                   img_scene):
    """
    Detecta features en la escena, empareja con el modelo usando ORB y SIFT
    y devuelve el conjunto de matches del detector ganador (más matches útiles).
    """
    kp_s_o, des_s_o = orb.detectAndCompute(img_scene, None)
    kp_s_s, des_s_s = sift.detectAndCompute(img_scene, None)

    # ── ORB con umbral Hamming fijo ──────────────────────────────────────────
    good_o = []
    if des_s_o is not None and des_m_o is not None:
        matches_o = bf_orb.knnMatch(des_m_o, des_s_o, k=2)
        good_o = [m for m, n in matches_o if m.distance < ORB_HAMMING_THRESHOLD]

    # ── SIFT con ratio test de Lowe ──────────────────────────────────────────
    good_s = []
    if des_s_s is not None and des_m_s is not None:
        matches_s = bf_sift.knnMatch(des_m_s, des_s_s, k=2)
        good_s = [m for m, n in matches_s if m.distance < SIFT_RATIO_TEST * n.distance]

    # ── Elige el detector con más matches útiles ─────────────────────────────
    if len(good_o) >= len(good_s):
        return good_o, kp_m_o, kp_s_o
    else:
        return good_s, kp_m_s, kp_s_s


def compute_homography(good, kp_m, kp_s):
    """Calcula la homografía y devuelve (M, src_pts, dst_pts) o (None, …)."""
    src_pts = np.float32([kp_m[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_s[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, RANSAC_REPROJ_THRESHOLD)
    return M, src_pts, dst_pts


def overlay_content(obj_virtual, M_smooth, img_scene):
    """
    Aplica warpPerspective y fusiona el contenido virtual con la escena.
    Devuelve la imagen de salida o None si hay un error.
    """
    try:
        h, w = img_scene.shape[:2]
        warped = cv2.warpPerspective(obj_virtual, M_smooth, (w, h))

        hM, wM = obj_virtual.shape[:2]
        mask = np.ones((hM, wM), dtype=np.uint8) * 255
        mask_warped = cv2.warpPerspective(mask, M_smooth, (w, h))
    except cv2.error as e:
        print(f"[WARN] warpPerspective falló: {e}")
        return None

    bg = cv2.bitwise_and(img_scene, img_scene, mask=cv2.bitwise_not(mask_warped))
    fg = cv2.bitwise_and(warped,    warped,    mask=mask_warped)
    return cv2.add(bg, fg)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("Uso: python armuseum.py <model> <scene> [patch|video|cam]")
        return

    img_model = cv2.imread(sys.argv[1])
    img_scene = cv2.imread(sys.argv[2])

    if img_model is None or img_scene is None:
        print("[ERROR] No se pudo cargar el modelo o la escena.")
        return

    hM, wM = img_model.shape[:2]

    # ── Fuente de contenido (vídeo, imagen o nada) ───────────────────────────
    cap       = None
    img_patch = None

    if len(sys.argv) >= 4:
        src = sys.argv[3]
        if src.isdigit():
            cap = cv2.VideoCapture(int(src))
        else:
            img_patch = cv2.imread(src)
            if img_patch is None:
                cap = cv2.VideoCapture(src)

    # ── Detectores y matchers ────────────────────────────────────────────────
    orb, sift, kp_m_o, des_m_o, kp_m_s, des_m_s = load_model_descriptors(img_model)
    bf_orb  = cv2.BFMatcher(cv2.NORM_HAMMING)
    bf_sift = cv2.BFMatcher()

    # ── Estado de suavizado ──────────────────────────────────────────────────
    M_smooth      = None
    bad_frames    = 0

    lines = [
        "La Escuela de Atenas",
        "Autor: Rafael Sanzio",
        "1509 - 1511",
    ]

    cv2.namedWindow("AR Museum", cv2.WINDOW_NORMAL)

    while True:
        # ── Matching ─────────────────────────────────────────────────────────
        good, kp_m, kp_s = match_features(
            orb, sift, bf_orb, bf_sift,
            kp_m_o, des_m_o, kp_m_s, des_m_s,
            img_scene
        )

        output = img_scene.copy()

        if len(good) > MIN_MATCHES_FOR_HOMOGRAPHY:
            M, src_pts, dst_pts = compute_homography(good, kp_m, kp_s)

            if is_valid_homography(M):
                err = reprojection_error(src_pts, dst_pts, M)

                if err < REPROJ_ERROR_THRESHOLD:
                    M_smooth   = smooth_matrix(M_smooth, M)
                    bad_frames = 0
                else:
                    # Si aún no tenemos ninguna H, aceptar aunque el error sea alto
                    # para no quedarse eternamente sin renderizar
                    if M_smooth is None:
                        M_smooth = M
                    print(f"[INFO] Homografía con error alto ({err:.1f} px), usando igual")
                    bad_frames += 1
                    if bad_frames > MAX_BAD_FRAMES:
                        M_smooth   = None
                        bad_frames = 0
            else:
                bad_frames += 1
                if bad_frames > MAX_BAD_FRAMES:
                    M_smooth   = None
                    bad_frames = 0

        # ── Renderizar siempre que haya una H válida, independientemente
        #    de si este frame tuvo matches suficientes o no ────────────────────
        if M_smooth is not None:
            obj_virtual = img_model.copy()

            # 1. Contenido interior: vídeo o imagen de patch
            if cap is not None and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()
                if ret:
                    vh, vw = hM // 8, wM // 8
                    frame  = cv2.resize(frame, (vw, vh))
                    x, y   = int(wM * 0.15), int(hM * 0.15)
                    obj_virtual[y:y+vh, x:x+vw] = frame

            elif img_patch is not None:
                # Redimensionar el patch pero conservar obj_virtual para
                # poder dibujar el texto encima
                patch_resized = cv2.resize(img_patch, (wM, hM))
                obj_virtual   = patch_resized.copy()

            # 2. Texto encima (siempre, sobre cualquier fondo)
            font      = cv2.FONT_HERSHEY_SIMPLEX
            scale     = 0.6
            thickness = 2
            start_y   = int(hM * 0.10)
            center_x  = wM // 2

            for i, line in enumerate(lines):
                (tw, th), _ = cv2.getTextSize(line, font, scale, thickness)
                x_txt = center_x - tw // 2
                y_txt = start_y + i * (th + 25)
                cv2.rectangle(obj_virtual,
                              (x_txt - 10, y_txt - th - 10),
                              (x_txt + tw + 10, y_txt + 10),
                              (0, 0, 0), -1)
                cv2.putText(obj_virtual, line, (x_txt, y_txt),
                            font, scale, (255, 255, 255),
                            thickness, cv2.LINE_AA)

            # 3. Warp + fusión
            result = overlay_content(obj_virtual, M_smooth, img_scene)
            if result is not None:
                output = result

        cv2.imshow("AR Museum", output)
        key = cv2.waitKey(1) & 0xFF

        if key in [27, ord('q')]:
            break
        elif key == ord('s'):
            save_dir = os.path.join("..", "data", "result")
            os.makedirs(save_dir, exist_ok=True)
            name = "capture_" + os.path.basename(sys.argv[2])
            path = os.path.join(save_dir, name)
            cv2.imwrite(path, output)
            print(f"[OK] Guardado en {path}")

    if cap:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
