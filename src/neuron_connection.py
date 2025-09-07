from src.neuron import Neuron


class NeuronConnection:
    def __init__(self, to_neuron: "Neuron", weight: float):
        self.to_neuron = to_neuron
        self.weight = weight
