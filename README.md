# VC_TRABAJO_CURSO

## Motivación

En la actualidad, la creciente demanda de interacciones fluidas entre humanos y máquinas nos lleva a la necesidad de interfaces que sean naturales y accesibles. Este proyecto surge como respuesta a este desafío, buscando crear una forma de interacción humano-máquina que no sólo sea eficiente, sino también intuitiva, sencilla y, en última instancia, entretenida al uso. Aprovechamos algunos de los conocimientos adquiridos durante la asignatura de Visión por Computador para explorar nuevas fronteras en la mejora de la experiencia de usuario en entornos informáticos. 

## Objetivos

El objetivo principal de esta propuesta es desarrollar una interfaz de usuario que permita manejar el ratón de un ordenador y realizar ajustes esenciales como ajustar el brillo de la pantalla y el volumen o acciones cotidianas como el sacar una captura de pantalla a través de la detección precisa de movimientos de nuestras manos utilizando la webcam.  

## Descripción técnica del trabajo

### 1.Creación del entorno conda

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

### 2.Tecnologías utilizadas/Materiales no originales

El proyecto ha sido desarrollado en python aprovechando algunas de las librerías que se proveen para este lenguaje de cara a manejar distintos ajustes, a continuación se enumeran las más importantes y su utilidad dentro de este proyecto:

- pyautogui: Nos permite manejar las coordenadas y eventos del ratón. Además, se utiliza también para realizar las capturas de pantalla.
- pycaw: Nos permite acceder a los altavoces del equipo y manejar aspectos como su volumen.
- screen-brightness-control: Nos permite ajustar el brillo de la pantalla.
- keyboard: Nos permite capturar las teclas que se pulsan de manera que podemos cambiar el modo en el que estamos ejecutando el programa.
- opencv-python: Nos permite caputar el vídeo de la webcam.
- mediapipe: Nos permite detectar las manos y distintos gestos que realice el usuario con ellas.

### 3.Desarrollo

Básicamente contamos con un script de python (control.py) que tiene distintos modos de ejecución. Por defecto, se comienza capturando la entrada de la webcam y se está en un modo "gestos" que nos permite realizar distintas acciones con nuestras manos que serán detectados utilizando MediaPipe más concretamente su ["Gesture Recognition"](https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer). En la versión actual este modo de funcionamiento detecta cuando cerramos y abrimos la mano realizando una captura de pantalla. Alternativamente se permite al usuario pulsar distintas teclas para acceder a los otros modos de funcionamiento de la siguiente forma:

- Pulsar la tecla "r": Nos llevará al modo de control del ratón, en este modo se detectará el dedo índice de forma que el ratón se desplazará hacia donde movamos nuestro dedo. Además, se procesa la distancia entre los dedos pulgar e índice de forma que si hacemos una pinza con estos dos dedos se hará un click izquierdo del ratón.
- Pulsar la tecla "b": Nos llevará al modo de control del brillo, en el cual se estará procesando la distancia entre los dedos pulgar e índice de forma que se interpola dicho valor entre 0 y 1, el valor que nos da lo multiplicamos por 100 y cambiamos el brillo al valor resultante.
- Pulsar la tecla "v": Nos llevará al modo de control de volumen, se hace un proceso similar al caso anterior, la principal diferencia es que el valor resultado en este caso lo asignamos al volumen del equipo.
- Pulsar cualquier otra tecla, exceptuando "Esc": Nos llevará nuevamente al modo por defecto.
- Pulsar la tecla "Esc": El programa finalizará su ejecución.

Cabe aclarar que de cara a capturar las teclas pulsadas por el usuario se ha creado un hilo, de forma que se intenta interferir lo menos posible en la ejecución del resto del programa.

### 4.Probelmas encontrados y trabajo futuro

Inicialmente, para calcular la posición que debía tener el ratón en función de la posición del dedo índice se hacía una interpolación de forma que conociendo la resolución del vídeo ofrecido por la webcam y la resolución de la pantalla se trasladaba fácilmente de una a otra. Sin embargo, se detectó que había problemas para alcanzar la parte inferior de la pantalla con el ratón. Esto se debe a que a medida que bajamos la mano, MediaPipe pierde contexto de la misma y deja de detectar. Como solución hemos usado para interpolar únicamente la mitad superior del vídeo capturado, esto hace que el movimiento en vertical sea más sensible, aún así no parece afectar demasiado al manejo del ratón pero sí que nos permite acceder a la parte inferior de la pantalla.

Uno de los problemas detectados con respecto al ratón es que a la hora de intentar hacer click cerrando la pinza entre los dedos pulgar e índice se desplaza también el ratón y por tatno no es tan sencillo hacer click en un lugar de forma muy precisa. Como trabajo futuro se plantearía que el click se haga en la coordenada que se encuentre a la distancia media entre ambos dedos.

Por otro lado, en un principio se pensó que el programa corriese en un único modo y que en función de cada gesto del usuario se ejecutaran las distintas funciones. Sin embargo, esto limitaba la funcionalidad de nuestro progama ya que no nos permitía repetir gestos que son muy intuitivos y aplicables a distintos controles como pueden ser el del brillo y el volumen. Por lo tanto, se optó como ya se ha comentado anteriormente en tener distintos modos a los que se accede pulsando distintas teclas.

Con respecto al gesto utilizado para realizar las capturas de pantalla tuvimos también algunos problemas. En un principio se planteó que la captura se hiciera al cerrar la mano, pero como la detección de MediaPipe se hace con tanta frecuencia la condición de "mano cerrada" se daba más de una vez y se hacían varias capturas sin pretenderlo. Además, notamos que las capturas de pantalla se sobreescribían al guardarse con el mismo nombre. Estos problemas se solucionaron controlando que entre captura y captura se tuviera que abrir la mano y pasara un tiempo de al menos un segundo y actualizando un contador de las capturas que se han realizado de forma que la forma en que se guardan es "screenshoot_n.png" donde n es el número de la captura. 

También cabe aclarar que al empezar el proyecto tratamos de usar la detección ["Hand Landmark Detection"](https://mediapipe-studio.webapps.google.com/studio/demo/hand_landmarker) de MediaPipe. No obstante, al tratar de introducirla en nuestro código se producían muchos cortes entre las detecciones pasando incluso segundos entre una detección y la siguiente. Por tanto, esta solución no nos permitía desarrollar nuestro proyecto por lo que pasamos como ya comentamos a usar ["Gesture Recognition"](https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer)


