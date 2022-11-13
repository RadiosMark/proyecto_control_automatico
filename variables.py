import matplotlib.pyplot as plt
from numpy import *

#### definimos algunas rutas que se usaran en main.py

ruta_x = 'c_v/x.txt'
ruta_y = 'c_v/y.txt'
ruta_theta = 'c_v/theta.txt'
ruta_u1 = 'm_v/u1.txt'
ruta_u2 = 'm_v/u2.txt'

vc_x = []
vc_y = []
vc_theta = []
vm_u1 = []
vm_u2 = []


def listas_datos(ruta, lista):
    with open(ruta, 'r', encoding='utf-8') as datos:
        lineas = datos.read().splitlines()
        for linea in lineas:
            lista.append(float(linea))

listas_datos(ruta_x, vc_x)
listas_datos(ruta_y, vc_y)
listas_datos(ruta_theta, vc_theta)
listas_datos(ruta_u1, vm_u1)
listas_datos(ruta_u2, vm_u2)

### la idea es cambiar la lista vc_x por las demas (intenté hacerlos todos de una pero todos se superponían y no sabía como ponerlos
### todos de una)

t = arange(len(vc_x))

plt.figure()
plt.title('Variable controlada X')
plt.plot(array(vc_x), t)
plt.show()


