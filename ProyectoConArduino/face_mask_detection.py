"""
Sistema de detección de mascarillas con OpenCV, MediaPipe y comunicación serial con Arduino.

Este programa usa una red neuronal entrenada para detectar si una persona usa mascarilla o no.
Cuando se detecta un rostro, se analiza con un modelo previamente entrenado y, según el resultado,
se envía un comando serial a un microcontrolador (Arduino) para encender una señal de control.

Dependencias:
- OpenCV
- MediaPipe
- PySerial

Funciones:
- find_model(model_path): Carga el modelo de reconocimiento facial desde un archivo XML.
- detect_face_mask(): Captura video en tiempo real, detecta rostros y evalúa si llevan mascarilla.
- conect_serial(): Establece conexión serial con el microcontrolador.

Autor: Patricio Milán
Fecha: 30/03/2025
"""
import cv2
import mediapipe as mp
import os
import serial
import time

def find_model(model_path):
    """
    Carga el modelo de reconocimiento de mascarillas desde un archivo XML.
    
    Parámetros:
    model_path (str): Ruta del archivo del modelo.
    """
    if os.path.exists(model_path):
        try:
            face_mask.read(model_path)
            print("Modelo cargado exitosamente.")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
    else:
        print("Error: No se encontró el archivo 'face_mask_model.xml")

def detect_face_mask():
    """
    Captura video en tiempo real, detecta rostros y evalúa si llevan mascarilla.
    
    Envía comandos seriales al microcontrolador según el resultado:
    - 'P' si la persona usa mascarilla.
    - 'N' si la persona no usa mascarilla.
    """
    global ser
    ultimo_estado = None
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        while True:                
            ret, frame = cap.read()
            if not ret:
                print("ERROR: No se pudo acceder a la cámara")
                break
            
            frame = cv2.flip(frame, 1) #Voltea la vizualización en espejo
                
            height, width, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame_rgb)
                    
            if results.detections is not None:
                for detection in results.detections:
                    xmin = int(detection.location_data.relative_bounding_box.xmin * width)
                    ymin = int(detection.location_data.relative_bounding_box.ymin * height)
                    w = int(detection.location_data.relative_bounding_box.width * width)
                    h = int(detection.location_data.relative_bounding_box.height * height)
                    
                    if xmin < 0 or ymin < 0:
                        continue
                            
                    try:
                        face_image = frame[ymin : ymin + h, xmin : xmin + w]
                        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                        face_image = cv2.resize(face_image, (70, 70), interpolation=cv2.INTER_AREA)
                        result = face_mask.predict(face_image)
                        
                        cv2.putText(frame, "{}".format(result), (xmin, ymin - 5), 1, 1.3, (210, 124,176), 1, cv2.LINE_AA)
                                
                        if result[1] < 150:
                            if ser is not None :
                                nuevo_estado = 'P' if LABELS[result[0]] == "with_mask" else 'N'
                                
                                # Solo enviar si hay un cambio de estado
                                if nuevo_estado != ultimo_estado:
                                    ser.write(nuevo_estado.encode() + b'\n')
                                    print(nuevo_estado)
                                    ultimo_estado = nuevo_estado  # Actualizar estado

                                color = (0, 255, 0) if nuevo_estado == 'P' else (0, 0, 255)
                                cv2.putText(frame, "{}".format(LABELS[result[0]]), (xmin, ymin - 25), 2, 1, color, 1, cv2.LINE_AA)
                                cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), color, 2)
                                
                            else:
                                print("No se pudo enviar el dato porque no hay conexión serial.")                
                    except:
                        print("Calibrando...")  

            #Mensaje para cierre de ventana
            cv2.putText(frame, "Presiona 'ESC' para finalizar", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == 27:  # Presionar 'ESC' para salir
                break
            
    ser.close()
    cap.release()
    cv2.destroyAllWindows()

def conect_serial():
    """
    Establece una conexión serial con el microcontrolador.
    """
    global ser
    try:
        ser = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)
        print("Conexión serial establecida correctamente.")
    except Exception as e:
        print(f"Error en la conexión serial: {e}")
        ser = None  #Evita que el código falle si la conexión no es posible

if __name__ == "__main__":
    conect_serial()
    mp_face_detection = mp.solutions.face_detection
    LABELS = ["without_mask", "with_mask"]
    face_mask = cv2.face.LBPHFaceRecognizer_create()
    model_path = "face_mask_model.xml"
    find_model(model_path)
    detect_face_mask()