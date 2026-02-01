from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter


def run_greenlee_emulator():
    server = GreenleeAmmeter(port=5000)
    server.start_server()

def run_entes_emulator():
    server = EntesAmmeter(port=5001)
    server.start_server()

def run_circutor_emulator():
    server = CircutorAmmeter(port=5002)
    server.start_server()