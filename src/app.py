from __future__ import annotations
from requests import get
from Cards import CardsManager

class App:
    LEVEL_REQUEST_URL = ' https://raw.githubusercontent.com/StonyTV/dofus-temporis-v-cards/main/levelup.json'

    def __init__(self) -> None:
        start_level = int(input('entrer le level de depart :\n>>> '))
        end_level = int(input('entrer le level d\'arriver :\n>>> '))
        self.cardsManager = CardsManager.load()
        self.levelRange = range(start_level, end_level + 1)
        self.card_id_needed = self.get_card_id_needed()
        self.card_needed = []
        self.card_dropable_needed = []
        self.card_craftable_needed = []
        self.load_card_needed()


    def get_card_id_needed(self) -> List[int]:
        response = get(App.LEVEL_REQUEST_URL, timeout=5)

        if not response.status_code:
            raise Exception('problem with fetching API (level)')

        level_datas = response.json()
        card_id_needed = []

        for level_data in level_datas:
            if level_data['level'] in self.levelRange:
                card_id_needed += level_data['cards']

        return card_id_needed

    def load_card_needed(self) -> None:
        for card_id in self.card_id_needed:
            card = self.cardsManager.get_card_by_id(card_id)
            self.card_needed.append(card)
            if card.obtention.isDrop:
                self.card_dropable_needed.append(card)
            else:
                self.card_craftable_needed.append(card)

    def get_items_required(self) -> Dict[str, int]:
        items_required = {}

        for card in self.card_craftable_needed:
            for item, quantity in card.obtention.obtention.items():
                if item not in items_required:
                    items_required[item] = int(quantity)
                else:
                    items_required[item] += int(quantity)

        return items_required

    def run(self) -> None:
        print('--------------carte demander pour up--------------')
        for card in self.card_needed:
            print(card.name)

        print('-------------------carte a drop-------------------')
        for card in self.card_dropable_needed:
                print(card.name)

        print('---------------ingredient requis-----------------')
        for name, quantity in self.get_items_required().items():
            print(f'{name} : x{quantity}')


