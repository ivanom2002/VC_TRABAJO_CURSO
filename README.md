# Trabajo de Curso de Visión por Computador

## Motivación

En la actualidad, la creciente demanda de interacciones fluidas entre humanos y máquinas nos lleva a la necesidad de interfaces que sean naturales y accesibles. Este proyecto surge como respuesta a este desafío, buscando crear una forma de interacción humano-máquina que no sólo sea eficiente, sino también intuitiva, sencilla y, en última instancia, entretenida al uso. Aprovechamos algunos de los conocimientos adquiridos durante la asignatura de Visión por Computador para explorar nuevas fronteras en la mejora de la experiencia de usuario en entornos informáticos. 

## Objetivos

El objetivo principal de esta propuesta es desarrollar una interfaz de usuario que permita manejar el ratón de un ordenador y realizar ajustes esenciales como ajustar el brillo de la pantalla y el volumen o acciones cotidianas como el sacar una captura de pantalla a través de la detección precisa de movimientos de nuestras manos utilizando la webcam.  

## Descripción técnica del trabajo

### 1. Creación del entorno conda

```
    conda create --name mediapipe python=3.11.5
    conda activate mediapipe
    pip install opencv-python
    pip install mediapipe
    pip install numpy
    pip install keyboard
    pip install pycaw
    pip install pyautogui
    pip install comptypes
    pip install screen-brightness-control
```

### 2. Tecnologías utilizadas/Materiales no originales

El proyecto ha sido desarrollado en python aprovechando algunas de las librerías que se proveen para este lenguaje de cara a manejar distintos ajustes de un ordenador. A continuación, se enumeran las más importantes y su utilidad dentro de este proyecto:

- [pyautogui](https://pyautogui.readthedocs.io/en/latest/): Nos permite manejar las coordenadas y eventos del ratón. Además, se utiliza también para realizar las capturas de pantalla.
- [pycaw](https://github.com/AndreMiras/pycaw): Nos permite acceder a los altavoces del equipo y manejar aspectos como su volumen.
- [screen-brightness-control](https://pypi.org/project/screen-brightness-control/): Nos permite ajustar el brillo de la pantalla.
- [keyboard](https://pypi.org/project/keyboard/): Nos permite capturar las teclas que se pulsan de manera que podemos cambiar el modo en el que estamos ejecutando el programa.
- [opencv-python](https://pypi.org/project/opencv-python/): Nos permite caputar el vídeo de la webcam.
- [mediapipe](https://pypi.org/project/mediapipe/): Nos permite detectar las manos y distintos gestos que realice el usuario con ellas.

### 3. Desarrollo

#### 3.1 Uso y funcionamiento

Básicamente contamos con un script de python (control.py) que tiene distintos modos de ejecución. Por defecto, se comienza capturando la entrada de la webcam y se está en un modo "gestos". Este modo nos permite realizar distintas acciones con nuestras manos que serán detectados utilizando MediaPipe. Más concretamente su ["Gesture Recognition"](https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer). En la versión actual este modo de funcionamiento se detecta cuando cerramos y abrimos la mano realizando una captura de pantalla. Alternativamente se permite al usuario pulsar distintas teclas para acceder a los otros modos de funcionamiento de la siguiente forma:

- Pulsar la tecla "r": Nos llevará al modo de control del ratón, en este modo se detectará el dedo índice de forma que el ratón se desplazará hacia donde movamos nuestro dedo. Además, se procesa la distancia entre los dedos pulgar e índice de forma que si hacemos una pinza con estos dos dedos se hará un click izquierdo del ratón.
- Pulsar la tecla "b": Nos llevará al modo de control del brillo, en el cual se estará procesando la distancia entre los dedos pulgar e índice de forma que se interpola dicho valor entre 0 y 1, el valor que nos da lo multiplicamos por 100 y cambiamos el brillo al valor resultante.
- Pulsar la tecla "v": Nos llevará al modo de control de volumen, se hace un proceso similar al caso anterior, la principal diferencia es que el valor resultado en este caso lo asignamos al volumen del equipo.
- Pulsar cualquier otra tecla, exceptuando "Esc": Nos llevará nuevamente al modo por defecto.
- Pulsar la tecla "Esc": El programa finalizará su ejecución.

#### 3.2 Aspectos clave del código

Con respecto a la estructura del código, tenemos un bucle principal que es el encargado de estar procesando la entrada de la webcam detectando así nuestras manos, sus coordenadas y otros parámetros como la distancia entre los dedos pulgar e índice.

```
# Inicializamos el objeto de captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():

    # Captura un fotograma
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el frame a RGB para la detección de manos
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

# Detener el bucle si se presiona la tecla 'Esc'
    if tecla == "esc":
        break

# Liberar la captura de video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
```

Por otro lado, tenemos las funciones encargadas de procesar la información recogida en el bucle principal ajustando así el brillo, el volumen o la posición del ratón según corresponda.

### 4.Probelmas encontrados y trabajo futuro

Inicialmente, para calcular la posición que debía tener el ratón en función de la posición del dedo índice se hacía una interpolación de forma que, conociendo la resolución del vídeo ofrecido por la webcam y la resolución de la pantalla se trasladaba fácilmente de una a otra. Sin embargo, se detectó que había problemas para alcanzar la parte inferior de la pantalla con el ratón. Esto se debe a que a medida que bajamos la mano, MediaPipe pierde contexto de la misma y deja de detectar. Como solución hemos usado para interpolar únicamente la mitad superior del vídeo capturado, esto hace que el movimiento en vertical sea más sensible, aún así no parece afectar demasiado al manejo del ratón pero sí que nos permite acceder a la parte inferior de la pantalla.

Otro de los problemas detectados con respecto al ratón es que a la hora de intentar hacer click cerrando la pinza entre los dedos pulgar e índice, se desplaza también el ratón y por tanto no es tan sencillo hacer click en un lugar de forma muy precisa. Como trabajo futuro se plantearía que el click se haga en la coordenada que se encuentre a la distancia media entre ambos dedos.

Por otro lado, en un principio se pensó que el programa corriese en un único modo y que en función de cada gesto del usuario se ejecutaran las distintas funciones. Sin embargo, esto limitaba la funcionalidad de nuestro progama ya que no nos permitía repetir gestos que son muy intuitivos y aplicables a distintos controles como pueden ser el del brillo y el volumen. Por lo tanto, se optó como ya se ha comentado anteriormente en tener distintos modos a los que se accede pulsando distintas teclas.

Con respecto al gesto utilizado para realizar las capturas de pantalla tuvimos también algunos problemas. En un principio se planteó que la captura se hiciera al cerrar la mano, pero como la detección de MediaPipe se hace con tanta frecuencia la condición de "mano cerrada" se daba más de una vez y se hacían varias capturas sin pretenderlo. Además, notamos que las capturas de pantalla se sobreescribían al guardarse con el mismo nombre. Estos problemas se solucionaron controlando que entre captura y captura se tuviera que abrir la mano y pasara un tiempo de al menos un segundo y actualizando un contador de las capturas que se han realizado de forma que el nombre de las capturas es "screenshoot_n.png" donde n es el número de la captura. 

También cabe aclarar que al empezar el proyecto tratamos de usar la detección ["Hand Landmark Detection"](https://mediapipe-studio.webapps.google.com/studio/demo/hand_landmarker) de MediaPipe. No obstante, al tratar de introducirla en nuestro código se producían muchos cortes entre las detecciones pasando incluso segundos entre una detección y la siguiente. Por tanto, esta solución no nos permitía desarrollar nuestro proyecto por lo que pasamos como ya comentamos a usar ["Gesture Recognition"](https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer)

De cara al futuro nos gustaría implementar más gestos como podrían ser desplazar el dedo índice en horizontal para cambiar entre las distintas ventanas, gestos que nos permitan acciones como cortar y pegar, hacer zoom en la pantalla, etc. Además de como ya se ha comentado mejorar la precisión en el uso del ratón.

## Conclusiones

Este proyecto puede representar un pequeño paso hacia la integración de la visión por computadora en la vida cotidiana. Al enfocarnos en la detección de movimientos de manos a través de la webcam, hemos demostrado cómo esta tecnología puede abordar problemas del día a día, acercando a las personas a la utilidad práctica de esta tecnología. Además, al desarrollar una interfaz de usuario que permite manejar el ratón, ajustar el brillo y volumen, y realizar acciones comunes, estamos contribuyendo al avance de interacciones más intuitivas y accesibles entre humanos y máquinas. 

## Fuentes

- [MediaPipe Studio](https://mediapipe-studio.webapps.google.com/home)
- ["Hand Landmark Detection"](https://mediapipe-studio.webapps.google.com/studio/demo/hand_landmarker)
- ["Gesture Recognition"](https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer)
- [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
- [pycaw](https://github.com/AndreMiras/pycaw)
- [screen-brightness-control](https://pypi.org/project/screen-brightness-control/)
- [keyboard](https://pypi.org/project/keyboard/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [mediapipe](https://pypi.org/project/mediapipe/)



