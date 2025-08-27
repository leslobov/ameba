class AmebaConfig:
    def __init__(
        self,
        neural_network_hidden_layers: int,
        neurons_on_layer: int,
        threhold_of_lostness_weight_coefficient: float,
        visible_width: int,
        visible_height: int,
        initial_energy: float,
    ):
        self.neural_network_hidden_layers = neural_network_hidden_layers
        self.neurons_on_layer = neurons_on_layer
        self.threhold_of_lostness_weight_coefficient = threhold_of_lostness_weight_coefficient
        self.visible_width = visible_width
        self.visible_height = visible_height
        self.initial_energy = initial_energy

    @staticmethod
    def neurons_qnt_add():
        pass

    @staticmethod
    def energy_lost_per_move():
        pass