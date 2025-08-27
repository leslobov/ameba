from .neuron_connection import NeuronConnection

class Neuron:
    def __init__(self, id: int, connections: list):
        self.id = id
        self.connections = connections  # List of NeuronConnection