import cv2
import time

# Tiempo de inicio
start_time = time.time()

# Inicializa la cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Verifica si la cámara se inicializó correctamente
if not cap.isOpened():
    print("No se pudo acceder a la cámara.")
    exit()

# Tiempo final y cálculo de la duración
end_time = time.time()
print(f"Cámara iniciada en {end_time - start_time} segundos.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame.")
        break

    cv2.imshow("Cámara", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
