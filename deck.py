import random
from config import tarot_cards

class TarotDeck:
    """Manages the tarot deck, including shuffling and drawing cards."""
    def __init__(self):
        self.cards = tarot_cards

    def draw_cards(self, num_cards=3):
        """Draws a specified number of unique cards from the deck."""
        return random.sample(self.cards, num_cards)
