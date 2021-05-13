from os import lockf
import threading
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

"""
    Clase listaFinita, extiende la clase list ([]) de modo que puede establecerse un limite máximo
    al tamaño (cantidad de objetos) de la lista.

    Uso:
    Declaración
    lista = listaFinita(Numero_Maximo_Items)
    # Crea una lista VACIA que admitirá hasta un máximo de Numero_Maximo_Items items

    El acceso a los elementos es igual que en una lista standard, la diferencia es que
    si se intenta agregar un elemento cuando la lista tiene Numero_Maximo_Items items, dara
    un mensaje de error y terminara el programa.

    Ejemplos
    Acceso al elemento i:

    a = lista[i]

    insertar un elemento en la posicón i.
    lista.insert(i, dato)  # si i es mayor que Numero_Maximo_Items termina el programa y da error

    o

    lista[i] = dato   # Si i es mayor que Numero_Maximo_Items termina el programa y da error.

    agregar un elemento al final de la lista

    lista.append(dato)  # Si la lista tiene Numero_Maximo_Items termina el programa y da error.

"""

class listaFinita(list):

    def __init__(self, max_elementos):
            self.max_elementos = max_elementos
            super().__init__()

    def pop(self, index):
        assert len(self) != 0, "lista vacia"
        return super().pop(index)

    def append(self, item):
        assert len(self) < self.max_elementos,"lista llena"
        super().append(item)

    def insert(self, index, item):
        assert index < self.max_elementos, "indice invalido"
        super().insert(index, item)

    def full(self):
        if len(self) == self.max_elementos:
            return True
        else:
            return False
    
    def isEmpty(self):
        var = False
        if len(self) == 0:
            var = True
        return var



class Productor(threading.Thread):
    def __init__(self, lista = listaFinita, lockProducto = threading.Lock() , lockConsumidor = threading.Lock()):
        super().__init__()
        self.lista = lista
        self.lockProducto = lockProducto
        self.lockConsumidor = lockConsumidor
        


    def run(self):
        while True:
            self.lockProducto.acquire()
            try:

                while self.lista.full():
                    pass
                self.lista.append(random.randint(0,100))
                logging.info(f'produjo el item: {self.lista[-1]}')
                time.sleep(random.randint(1,5))
            finally:
                self.lockConsumidor.release()
        #while True:
        #    self.lista.append(random.randint(0,100))
        #    logging.info(f'produjo el item: {self.lista[-1]}')
        #    time.sleep(random.randint(1,5))


class Consumidor(threading.Thread):
    def __init__(self, lista, lockConsumidor = threading.Lock() , lockProducto = threading.Lock()):
        super().__init__()
        self.lista = lista
        self.lockConsumidor = lockConsumidor
        self.lockProducto = lockProducto

    def run(self):
        while True:
            self.lockConsumidor.acquire()
            try:
                while self.lista.isEmpty():
                    pass
                elemento = self.lista.pop(0)
                logging.info(f'consumio el item {elemento}')
                time.sleep(random.randint(1,5))
            finally:
                self.lockProducto.release()
        #while True:
        #    elemento = self.lista.pop(0)
        #    logging.info(f'consumio el item {elemento}')
        #    time.sleep(random.randint(1,5))

def main():
    hilos = []
    lista = listaFinita(4)
    lockProd = threading.Lock()
    lockCons = threading.Lock()
    

    for i in range(4):
        productor = Productor(lista, lockProd, lockCons)
        consumidor = Consumidor(lista, lockCons, lockProd)
        hilos.append(productor)
        hilos.append(consumidor)

        logging.info(f'Arrancando productor {productor.name}')
        productor.start()

        logging.info(f'Arrancando productor {consumidor.name}')
        consumidor.start()

    for h in hilos:
        h.join()


if __name__ == '__main__':
    main()
