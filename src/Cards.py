from __future__ import annotations
from requests import get
from Card import Card

class CardsManager:
    REQUEST_URL = 'https://raw.githubusercontent.com/StonyTV/dofus-temporis-v-cards/main/db.json'

    def __init__(self, cards: List[cards]) -> None:
        self.cards = cards

    @classmethod
    def load(cls) -> CardsManager:
        response = get(CardsManager.REQUEST_URL, timeout=5)

        if not response.status_code:
            raise Exception('Problem with fetching API (database card)')

        cards_data = response.json()
        cards = []

        for card_json in cards_data['indexDB']:
            cards.append(Card.deserialize_from_json(card_json))

        return cls(cards)

    def get_card_by_id(self, card_id: int) -> Card:
        for card in self.cards:
            if card.ID == card_id:
                return card
