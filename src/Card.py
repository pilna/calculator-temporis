from __future__ import annotations

class Obtention:

    def __init__(self, obtention: Dict[str, float], isDrop: bool = False) -> None:
        self.isDrop = isDrop
        self.obtention = obtention

    @classmethod
    def deserialize_from_json(cls, json: Dict[str, Any]) -> Obtention:
        if 'obt' not in json:
            return cls({'???', 0}, True)

        string = json['obt']
        isDrop = '%' in string
        obtention_list = string.replace(', ', ',').replace(' (', '(').split(',')
        obtentions = {}

        for obtention in obtention_list:
            name, tail = obtention.split('(')
            value = float(tail.replace('x', '').replace('%', '').replace(')', ''))
            obtentions[name] = value
        
        return cls(obtentions, isDrop)

    def __str__(self) -> None:
        string = ""

        for entity_name, value in self.obtention.items():
            string += f'{entity_name} : {"x" if not self.isDrop else ""}{value}{"%" if self.isDrop else ""}\n'

        return string


class Card:

    def __init__(self, name: str, obtention: Obtention, ID: int, item_id: int, rarity: str, color: str, job: str, level: int) -> None:
        self.name = name
        self.obtention = obtention
        self.ID = ID
        self.item_id = item_id
        self.rarity = rarity
        self.color = color
        self.job = job
        self.level = level

    @classmethod
    def deserialize_from_json(cls, json: Dict[str, Any]) -> Card:
        name = json['name']
        obtention = Obtention.deserialize_from_json(json)
        ID = json['id']
        item_id = json['idItem'] if 'idItem' in json else None
        rarity = json['color']
        color = json['type']
        job = json['profession']
        level = json['level']
        return cls(name, obtention, ID, item_id, rarity, color, job, level)

    def __str__(self) -> str:
        return f"{self.ID} : {self.name} ({self.level})\n{str(self.obtention)}"
