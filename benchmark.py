import cv2
import numpy as np
import time
import os

# ─── Parámetros configurables ────────────────────────────────────────────────
MIN_RATIO_MATCHES  = 25   # mínimo de matches tras ratio test para considerar homografía
MIN_INLIERS        = 20   # mínimo de inliers RANSAC para considerar homografía válida
ORB_HAMMING_THRESH = 50   # umbral Hamming fijo para ORB (distancia 0-255)
SIFT_RATIO         = 0.75 # ratio test de Lowe para SIFT
RANSAC_THRESHOLD   = 5.0  # umbral de reproyección RANSAC (píxeles)

# ─── Rutas relativas ─────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE_DIR, "..", "data")
MODEL_DIR = os.path.join(DATA_DIR, "model")
SCENE_DIR = os.path.join(DATA_DIR, "scenes")

img_model = cv2.imread(os.path.join(MODEL_DIR, "LaEscuela100.jpg"))

if img_model is None:
    print("[ERROR] No se encontró el modelo. Comprueba la ruta DATA_DIR.")
    exit(1)

escenas = [os.path.join(SCENE_DIR, f"LaEscuela{i}.jpg") for i in range(1, 13)]

# ─── Detectores y matchers ────────────────────────────────────────────────────
orb  = cv2.ORB_create(nfeatures=4000)
sift = cv2.SIFT_create()
bf_orb  = cv2.BFMatcher(cv2.NORM_HAMMING)
bf_sift = cv2.BFMatcher()

kp_m_o, des_m_o = orb.detectAndCompute(img_model, None)
kp_m_s, des_m_s = sift.detectAndCompute(img_model, None)


# ─── Cabecera de la tabla ─────────────────────────────────────────────────────
W = 130
print("BENCHMARK COMPLETO - AR MUSEUM (ORB vs SIFT lado a lado)")
print(f"{'Imagen':<22} {'Det':<6} {'Brutos':<8} {'Ratio':<8} {'RANSAC':<8} {'Homogr.':<10} {'T(ms)':<10} {'Ganador'}")
print("-" * W)


# ─── Procesar cada escena ─────────────────────────────────────────────────────
for ruta in escenas:
    nombre    = os.path.basename(ruta)
    img_scene = cv2.imread(ruta)

    if img_scene is None:
        print(f"{nombre:<22} {'ERROR — no carga'}")
        continue

    inicio_total = time.time()

    kp_s_o, des_s_o = orb.detectAndCompute(img_scene, None)
    kp_s_s, des_s_s = sift.detectAndCompute(img_scene, None)

    # ── ORB ──────────────────────────────────────────────────────────────────
    brutos_o = ratio_o = ransac_o = 0

    if des_s_o is not None:
        matches_o = bf_orb.knnMatch(des_m_o, des_s_o, k=2)
        brutos_o  = len(matches_o)
        # Umbral Hamming fijo (no ratio test de Lowe, que no escala igual en L2)
        buenos_o  = [m for m, n in matches_o if m.distance < ORB_HAMMING_THRESH]
        ratio_o   = len(buenos_o)

        if ratio_o > 4:
            src_o = np.float32([kp_m_o[m.queryIdx].pt for m in buenos_o]).reshape(-1, 1, 2)
            dst_o = np.float32([kp_s_o[m.trainIdx].pt for m in buenos_o]).reshape(-1, 1, 2)
            _, mask_o = cv2.findHomography(src_o, dst_o, cv2.RANSAC, RANSAC_THRESHOLD)
            ransac_o = int(mask_o.sum()) if mask_o is not None else 0

    # ── SIFT ─────────────────────────────────────────────────────────────────
    brutos_s = ratio_s = ransac_s = 0

    if des_s_s is not None:
        matches_s = bf_sift.knnMatch(des_m_s, des_s_s, k=2)
        brutos_s  = len(matches_s)
        buenos_s  = [m for m, n in matches_s if m.distance < SIFT_RATIO * n.distance]
        ratio_s   = len(buenos_s)

        if ratio_s > 4:
            src_s = np.float32([kp_m_s[m.queryIdx].pt for m in buenos_s]).reshape(-1, 1, 2)
            dst_s = np.float32([kp_s_s[m.trainIdx].pt for m in buenos_s]).reshape(-1, 1, 2)
            _, mask_s = cv2.findHomography(src_s, dst_s, cv2.RANSAC, RANSAC_THRESHOLD)
            ransac_s = int(mask_s.sum()) if mask_s is not None else 0

    # ── Homografía detectable? ────────────────────────────────────────────────
    homo_o = "Sí" if (ratio_o >= MIN_RATIO_MATCHES and ransac_o >= MIN_INLIERS) else "No"
    homo_s = "Sí" if (ratio_s >= MIN_RATIO_MATCHES and ransac_s >= MIN_INLIERS) else "No"

    # ── Ganador ───────────────────────────────────────────────────────────────
    if ratio_o > ratio_s:
        ganador = "ORB 🏆"
    elif ratio_s > ratio_o:
        ganador = "SIFT 🏆"
    else:
        ganador = "EMPATE"

    tiempo_ms = (time.time() - inicio_total) * 1000

    # ── Imprimir dos filas (una por detector) ─────────────────────────────────
    print(f"{nombre:<22} {'ORB':<6} {brutos_o:<8} {ratio_o:<8} {ransac_o:<8} {homo_o:<10} {tiempo_ms:<10.1f}")
    print(f"{'':<22} {'SIFT':<6} {brutos_s:<8} {ratio_s:<8} {ransac_s:<8} {homo_s:<10} {'':<10} {ganador}")


# ─── Leyenda ──────────────────────────────────────────────────────────────────
print("\n" + "=" * W)
print("LEYENDA:")
print(f"  Brutos   : matches de knnMatch(k=2)")
print(f"  Ratio    : matches tras filtro (ORB: Hamming < {ORB_HAMMING_THRESH} | SIFT: ratio < {SIFT_RATIO})")
print(f"  RANSAC   : inliers geométricamente consistentes (umbral {RANSAC_THRESHOLD} px)")
print(f"  Homogr.  : 'Sí' si Ratio >= {MIN_RATIO_MATCHES} y RANSAC >= {MIN_INLIERS}")
print(f"  Ganador  : detector con más matches tras filtro")
