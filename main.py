import cv2
from collections import deque

# Definir los límites de color en el espacio HSV
colors = {
    "green": ((29, 86, 6), (64, 255, 255)),
    "blue": ((90, 50, 50), (130, 255, 255)),
    "red": ((0, 50, 50), (10, 255, 255)),
    "yellow": ((20, 100, 100), (30, 255, 255))
}

# Inicializar el buffer para los puntos de seguimiento
buffer_size = 64
pts = {color: deque(maxlen=buffer_size) for color in colors}

# Inicializar la captura de video (usando DirectShow para mayor compatibilidad en Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar y procesar el frame
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color, (lower, upper) in colors.items():
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Encontrar contornos y calcular el centro de los objetos
        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                # Dibujar el círculo y el centro del objeto detectado
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts[color].appendleft(center)

                # Dibujar la línea de seguimiento
                for i in range(1, len(pts[color])):
                    if pts[color][i - 1] is None or pts[color][i] is None:
                        continue
                    cv2.line(frame, pts[color][i - 1], pts[color][i], (0, 255, 0), 2)

    # Mostrar el frame con el seguimiento
    cv2.imshow("Seguimiento de Pelota", frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Limpiar recursos
cap.release()
cv2.destroyAllWindows()
