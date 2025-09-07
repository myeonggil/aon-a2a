import collections


Card = collections.namedtuple('Card', ['rank', 'suit'])

card = Card(rank='2', suit='Spad')

class Deck:
    def __init__(self, cards: list[Card]):
        self.decks = cards

    def __len__(self):
        return len(self.decks)

    def __getitem__(self, position):
        return self.decks[position]

    def __repr__(self):
        return f"Cards"

ranks = ['J', 'Q', 'K', 'A']
suits = ['Spade', 'Heart', 'A', 'B']
cards = [Card(rank=rank, suit=suit) for rank in ranks for suit in suits]
deck = Deck(cards=cards)
