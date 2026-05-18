1. Uso general
python armuseum.py <model> <scene> [patch|video|cam]

PARÁMETROS:

model  → Imagen del objeto a detectar (pintura)
scene  → Imagen donde se busca el objeto
patch  → (opcional) imagen que se muestra como contenido virtual
video  → (opcional) vídeo que se muestra como contenido virtual
cam    → (opcional) índice de cámara web (0, 1, ...)

2. EJEMPLOS:

. Solo detección + texto:
python armuseum.py ../data/model/LaEscuela100.jpg ../data/scenes/LaEscuela1.jpg

. Con vídeo:
python armuseum.py ../data/model/painting.jpg ../data/scenes/scene1.jpg ../data/video/speedTest.mp4

. Con webcam:
python armuseum.py ../data/model/LaEscuela100.jpg ../data/scenes/LaEscuela4.jpg 0

. Con imagen (patch):
python armuseum.py ../data/model/LaEscuela100.jpg ../data/scenes/LaEscuela11.jpg ../data/scenes/LaEscuela10.jpg


3. FUNCIONALIDAD

Teclas:
- S → guardar captura en /data/result
- ESC o q → salir del programa


4. DEPENDENCIAS

- Python 3.x
- OpenCV
- NumPy

# programas
