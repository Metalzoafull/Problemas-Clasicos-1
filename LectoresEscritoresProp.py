from os import write
import threading
import random
import logging
import time
from rwlock import RWLock



logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

equipos = ["Boca", "River", "Racing", "Independiente", "San Lorenzo", "Huracán", "Gimnasia",
           "Estudiantes", "Velez", "Ferro", "Lanus", "Quilmes"]


partido = ["", 0, "", 0]

rwLock = RWLock()


def escritor(id):
    global partido
    global equipos
    name = 'Escritor- ' + str(id)
    
    while (True):
        equi1 = random.randint(0, len(equipos)-1)
        equi2 = random.randint(0, len(equipos)-1)

        while equi1 == equi2:
            equi2 = random.randint(0, len(equipos)-1)
        rwLock.w_acquire()

        try:
            partido[0] = equipos[equi1]
            partido[1] = random.randint(0, 4)
            partido[2] = equipos[equi2]
            partido[3] = random.randint(0, 4)
            logging.info(f'{name} Actualizo el partido')

        finally:
            ##time.sleep(random.randint(1, 2))
            rwLock.w_release()
            time.sleep(random.randint(1, 2))


def lector(id):
    global partido
    global equipos
    name = 'Escritor- ' + str(id)

    while (True):
        rwLock.r_acquire()
        try:
            logging.info(f'{name} el resultado fue: {partido[0]} {partido[1]} - {partido[2]} {partido[3]}')

        finally:
            ##time.sleep(random.randint(1, 2))
            rwLock.r_release()
            time.sleep(random.randint(1, 2))


def main():
    hilos = []
    for i in range(1):
        writer = threading.Thread(target = escritor, args=(i,))
        logging.info(f'Arrancando escritor- {i}')
        writer.start()
        hilos.append(writer)

    for i in range(4):
        reader = threading.Thread(target= lector, args=(i,))
        logging.info(f'Arrancando lector- {i}')
        reader.start()
        hilos.append(escritor)

    for i in hilos:
        i.join()


if __name__ == "__main__":
    main()    