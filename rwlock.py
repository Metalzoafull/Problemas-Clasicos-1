""" rwlock.py
    Clase para implementar read-write locks sobre la libreria standard threading.
    rLock: Read Lock, permite multiples accesos concurrentes a operaciones de Lectura (Read)
    wLock: Write Lock, permite un unico acceso (exclusión mútuo) para Escritura (Write)
    Esto esta implementado con dos MUTEX (instancias threading.Lock) y una variable entera (num_r) que lleva
    la cuenta de la cantidad de Readers bloqueados. Un Lock (num_r_lock) protege el acceso a num_r y solo es
    utlizado por los Readers. El otro Lock (w_lock) es de acceso global y asegura la exclusión mutua de los
    writers. Esto requiere que un Lock adquirido por una thread pueda ser liberado por otra.

    Comenzar Lectura (adquirir Read Lock)
    1 obtener num_r_lock
    2 incrementar num_r
    3 Si num_r = 1, obtener w_lock
    4 liberar num_r_lock

    Fin de Lectura (Liberar Read Lock)
    1 obtener num_r_lock
    2 decrementar num_r
    3 Si num_r = 0, liberar w_lock
    4 liberar num_r_lock

    Comenzar Escritura
    1 obtener w_lock

    Fin de Escritura
    2 liberar w_lock

    Esta es una implementación de RW Locks con Preferencia de Lectura (Read-Preferring RW locks).
    Este tipo de RW lock permite la máxima concurrencia, pero pueden provocar falta de escritura (Write-Starvation)
    si la concurerncia es alta.
    Esto se debe a que los hilos writer no pueden adquirir el Lock mientras al menos un hilo reader lo tenga.
    Dado que varios hilos reader pueden tener el lock a la vez, un hilo writer puede quedarse esperando el lock
    mientras nuevos hilos reader pueden obtenerlo, incluso hasta el punto en que el writer tenga que esperar
    hasta que todos los readers que tienen el lock lo liberen.

    Nota: Hay otras implementaciones de RW Locks:

        Write-preferring RW Locks (resuelve el problema de writer-starvation)
        Unspecified-priority RW Locks

"""


# _______________________________________________________________________
# Imports

from threading  import Lock

# _______________________________________________________________________
# Class

class RWLock(object):
    """ Clase RWLock;  tiene como propósito permitir que un objeto sea leido por multiples hilos
        simultáneamente, pero solo puede ser escrito por un solo hilo a la vez.

        Uso:
            from rwlock import RWLock
            mi_RWLock = RWLock()

            # Al leer de mi_objeto
            mi_RWLock.r_acquire()
            try:
                # tareas de SOLO Lectura con mi_objeto
            finally:
                mi_RWLock.r_release()


            # Al escribir en my_obj:
            mi_RWLock.w_acquire()
            try:
                # tareas de escritura en mi_objeto
            finally:
                mi_RWLock.w_release()

    """
    # Constructor

    def __init__(self):

        self.w_lock = Lock()
        self.num_r_lock = Lock()
        self.num_r = 0

    # ___________________________________________________________________
    # Metodos de Lectura (Reading).

    def r_acquire(self):
        self.num_r_lock.acquire()
        self.num_r += 1
        if self.num_r == 1:
            self.w_lock.acquire()
        self.num_r_lock.release()

    def r_release(self):
        assert self.num_r > 0
        self.num_r_lock.acquire()
        self.num_r -= 1
        if self.num_r == 0:
            self.w_lock.release()
        self.num_r_lock.release()


    # ___________________________________________________________________
    # Métodos de Escritura (Writing).

    def w_acquire(self):
        self.w_lock.acquire()

    def w_release(self):
        self.w_lock.release()

#1.B1) cuenta la cantidad de veces que el READ LOCK() fue llamado.

#1.B2) lo obtendra el primero que lo pida, el resto de procesos lectores estaran en estado de espera hasta que sea liberado el w_lock

#1.B3) el proceso lector liberara el w_lock en el proceso r_release, cuando el num_r sea igual a 0 sera en ese entonces que liberara a w_lock

#1.B4) dependeria de quien tome control del w_lock, si los N procesos toman el control primero entonces el proceso escritor tendra que esperar a que todos los N procesos de lectura terminen, debido a que los procesos de lectura tomaran el w_lock y no lo liberaran hasta que se hayan realizado todos los r_release().
