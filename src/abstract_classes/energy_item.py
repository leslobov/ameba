from abc import ABC, abstractmethod


class EnergyItem(ABC):
    @abstractmethod
    def get_energy(self) -> float:
        pass

    @abstractmethod
    def mark_deleted(self) -> None:
        pass

    @abstractmethod
    def is_deleted(self) -> bool:
        pass
