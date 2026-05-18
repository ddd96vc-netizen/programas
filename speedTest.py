import cv2
import time
import os

# ─── Ruta relativa ────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "data", "model", "LaEscuela100.jpg")

img = cv2.imread(MODEL_PATH)

if img is None:
    print(f"[ERROR] No se encontró la imagen en: {MODEL_PATH}")
    exit(1)

REPETICIONES = 50

orb  = cv2.ORB_create(nfeatures=4000)
sift = cv2.SIFT_create()

# ─── Medir ORB ────────────────────────────────────────────────────────────────
inicio = time.time()
for _ in range(REPETICIONES):
    kp, des = orb.detectAndCompute(img, None)
tiempo_orb = (time.time() - inicio) / REPETICIONES * 1000  # ms/frame

# ─── Medir SIFT ───────────────────────────────────────────────────────────────
inicio = time.time()
for _ in range(REPETICIONES):
    kp, des = sift.detectAndCompute(img, None)
tiempo_sift = (time.time() - inicio) / REPETICIONES * 1000  # ms/frame

# ─── Resultados ───────────────────────────────────────────────────────────────
print(f"ORB  : {tiempo_orb:.2f} ms/frame  →  {1000 / tiempo_orb:.1f} FPS teóricos")
print(f"SIFT : {tiempo_sift:.2f} ms/frame  →  {1000 / tiempo_sift:.1f} FPS teóricos")
print(f"SIFT es {tiempo_sift / tiempo_orb:.1f}x más lento que ORB")
