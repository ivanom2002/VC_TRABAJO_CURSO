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

### 2.Tecnologías utilizadas

El proyecto ha sido desarrollado en python aprovechando algunas de las librerías que se proveen para este lenguaje de cara a manejar distintos ajustes, a continuación se enumeran las más importantes y su utilidad dentro de este proyecto:

- pyautogui: Nos permite manejar las coordenadas y eventos del ratón. Además, se utiliza también para realizar las capturas de pantalla.
- pycaw: Nos permite acceder a los altavoces del equipo y manejar aspectos como su volumen.
- screen-brightness-control: Nos permite ajustar el brillo de la pantalla.
- keyboard: Nos permite capturar las teclas que se pulsan de manera que podemos cambiar el modo en el que estamos ejecutando el programa.
- opencv-python: Nos permite caputar el vídeo de la webcam.
- mediapipe: Nos permite detectar las manos y distintos gestos que realice el usuario con ellas.

### 3.Materiales no originales
