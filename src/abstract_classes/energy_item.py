from abc import ABC, abstractmethod


class EnergyItem(ABC):
    @abstractmethod
    def get_energy(self) -> float:
        pass
