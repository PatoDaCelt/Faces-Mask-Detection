"""
Este script entrena un modelo de reconocimiento facial utilizando la técnica Local Binary Patterns Histogram (LBPH) 
para detectar si una persona usa o no mascarilla. 

Flujo del programa:
1. Se leen imágenes almacenadas en subdirectorios dentro de la carpeta dataset.
2. Se convierten las imágenes a escala de grises y se asignan etiquetas a cada categoría.
3. Se entrena el modelo LBPH con las imágenes y etiquetas.
4. Se almacena el modelo entrenado en un archivo XML para su posterior uso en la detección de mascarillas.

Librerías utilizadas:
- OpenCV (cv2): Para manipulación de imágenes y entrenamiento del modelo.
- NumPy: Para manejo de matrices y etiquetas.
- OS: Para gestión de archivos y directorios.
"""
import cv2
import os
import numpy as np

#Ruta del directorio que almacena las imagenes
dataPath = "C:/Users/patmi/OneDrive/Documentos/Proyectos/DeteccionMascarillaIntegrandoArduino/dataset"

#Lista de subdirectorios en dataPath
dir_list = os.listdir(dataPath)
print("Lista de archivos", dir_list)  #Muestra los subdirectorios

labels = []    #Lista para almacenar las etiquetas
facesData = [] #Lista para almacenar las imagenes
label = 0

for name_dir in dir_list:
    #Formar la ruta completa del subdirectorio actual
    dir_path = dataPath + "/" + name_dir
    
    for file_name in os.listdir(dir_path):
        #Formar la ruta completa de cada imagen en el sudirectorio
        image_path = dir_path + "/" + file_name
        #print(image_path)   #Muestra la ruta completa de la imagen
        #Leer imagen en escala de grises
        image = cv2.imread(image_path, 0)
        
        #cv2.imshow("Image", image)  #Muestra las imagenes
        #cv2.waitKey(10)
        
        #Agregar todas las imagenes en facesData y las etiquetas en labels
        facesData.append(image)
        labels.append(label)
        
    label += 1  #Se asigna una nueva etiqueta a cada subdirectorio
    
print("Etiqueta 0: ", np.count_nonzero(np.array(labels) == 0))
print("Etiqueta 1: ", np.count_nonzero(np.array(labels) == 1))

#Local Binary Path History Face Recognizer
face_mask = cv2.face.LBPHFaceRecognizer_create()

#ENTRENAMIENTO
print("ENTRENANDO...")
face_mask.train(facesData, np.array(labels))

#Almacenar modelo
face_mask.write("face_mask_model.xml")
print("Modelo almacenado")