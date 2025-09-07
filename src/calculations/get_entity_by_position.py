from typing import Optional, Sequence
from src.types.desk_entity import DeskEntity

from src.shared_classes.position import Position


def get_entity_by_position(
    position: Position, entities: Sequence[DeskEntity]
) -> Optional[DeskEntity]:
    for entity in entities:
        if (
            entity.get_position().column == position.column
            and entity.get_position().row == position.row
        ):
            return entity
    return None
