import pyautogui
import cv2
from mediapipe import solutions
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import keyboard
import threading
import time

# Inicializamos las variables de las manos
mpHands = solutions.hands
hands = mpHands.Hands()
tecla = None
last_screenshot = time.time()
hand_was_open = False
num_screenshoots = 0

# Inicializamos el objeto de captura de video
cap = cv2.VideoCapture(0)  

def capturar_tecla():
    global tecla
    while True:
        try:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                tecla = event.name
        except KeyboardInterrupt:
            break
        
def volume_control(distance):
    min_distance = 40
    max_distance = 200  

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    new_volume = max(0, min((distance - min_distance) / (max_distance - min_distance), 1))
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def brightness_control(distance):
    min_distance = 40
    max_distance = 200
    new_brightness = max(0, min((distance - min_distance) / (max_distance - min_distance), 1))
    sbc.set_brightness(new_brightness * 100)

def mouse_control(x, y, distance):
    if (distance > 40):
      pyautogui.moveTo(x, y)
    else:
      pyautogui.click()

def screenshoot():
    global num_screenshoots
    screenshot_name = f"screenshoot_{num_screenshoots}.png"
    pyautogui.screenshot(screenshot_name)

hilo_captura = threading.Thread(target=capturar_tecla, daemon=True)
hilo_captura.start()

while cap.isOpened():

    # Captura un fotograma
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el frame a RGB para la detección de manos
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    # Verificar si se detectaron manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener las coordenadas del dedo índice
            index_tip_x = int(hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
            index_tip_y = int(hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])
            index_mcp_y = int(hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].y * frame.shape[0])

            # Obtener las coordenadas del dedo pulgar
            thumb_tip_x = int(hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x * frame.shape[1])
            thumb_tip_y = int(hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].y * frame.shape[0])
            thumb_mcp_y = int(hand_landmarks.landmark[mpHands.HandLandmark.THUMB_MCP].y * frame.shape[0])

            # Obtener las coordenadas del dedo corazon
            middle_tip_x = int(hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].x * frame.shape[1])
            middle_tip_y = int(hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y * frame.shape[0])
            middle_mcp_y = int(hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_MCP].y * frame.shape[0])

            # Obtener las coordenadas del dedo anular
            ring_tip_x = int(hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP].x * frame.shape[1])
            ring_tip_y = int(hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y * frame.shape[0])
            ring_mcp_y = int(hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])

            # Obtener las coordenadas del dedo meñique
            pinky_tip_x = int(hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP].x * frame.shape[1])
            pinky_tip_y = int(hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP].y * frame.shape[0])
            pinky_mcp_y = int(hand_landmarks.landmark[mpHands.HandLandmark.PINKY_MCP].y * frame.shape[0])

            if (index_tip_y > index_mcp_y and ring_tip_y > ring_mcp_y and middle_tip_y > middle_mcp_y and pinky_tip_y > pinky_mcp_y):
                if time.time() - last_screenshot > 1 and hand_was_open and tecla != "r" and tecla != "b" and tecla != "v":
                    screenshoot()
                    num_screenshoots += 1
                    last_screenshot = time.time()
                hand_was_open = False
            else:
                hand_was_open = True

            # Calcular la distancia entre el pulgar y el índice
            distance = np.sqrt((thumb_tip_x - index_tip_x)**2 + (thumb_tip_y - index_tip_y)**2)

            x = 1920 - (((index_tip_x ) * pyautogui.size()[0]) // (frame.shape[0]))
            y = ((index_tip_y * pyautogui.size()[1]) * 2) // frame.shape[1]

            #Comprobar que x, y se encuentran dentro del tamaño de pantalla
            if (x < 1920 and y < 1080):
               #Procesar la función correspondiente
              if (tecla == "r"):
                mouse_control(x, y, distance)
              elif (tecla == "v"):
                volume_control(distance)
              elif (tecla == "b"):
                brightness_control(distance)
              else:
                continue

    # Detener el bucle si se presiona la tecla 'Esc'
    if tecla == "esc":
        break

# Liberar la captura de video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()

