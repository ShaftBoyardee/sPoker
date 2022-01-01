from typing import TypeVar, List
import random

T = TypeVar("T")
Card = TypeVar("Card")
Deck = TypeVar("Deck")

class Card:
    """Playing card class"""
    def __init__(self, name: str="Joker", suit: str=None, value: int=0) -> None:
        self.name = name
        self.suit = suit
        self.value = value
    
    def __str__(self) -> str:
        """
        String representation of card
        """
        suits = {"spades": "♠", "hearts": "♥", "diamonds": "♦", "clubs": "♣"}
        out = str()
        if self.suit:
            out += suits[self.suit]
        out += self.name
        return out
    
    def __repr__(self) -> str:
        """
        String representation of card
        """
        return str(self)

    def __eq__(self, o: Card) -> bool:
        """
        Comparison for normal point values
        """
        if self.value == o.value:
            return True
        return False
    
    def __gt__(self, o: Card) -> bool:
        """
        Greater than comparison for normal point values
        """
        return self.value > o.value
    
    def __lt__(self, o: Card) -> bool:
        """
        Greater than comparison for normal point values
        """
        return self.value < o.value

class Deck:
    """Playing card deck class"""
    def __init__(self, jokers: bool=False, ace_high: bool=False) -> None:
        suits = ["spades", "hearts", "diamonds", "clubs"]
        face_values = {"J": 11, "Q": 12, "K": 13, "A": 1 if not ace_high else 14}
        cards = [str(i) for i in range(2, 11)]
        cards.append("J")
        cards.append("Q")
        cards.append("K")
        cards.append("A")
        self.cards = [Card(name=n, suit=s, value=face_values.get(n) or int(n)) for s in suits for n in cards]
        if jokers:
            for i in range(2):
                self.cards.append(Card())
    
    def __str__(self) -> str:
        out = str()
        for card in self.cards:
            out += str(card) + "\n"
        return out.strip()
    
    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return len(self.cards)
    
    def __getitem__(self, idx: int) -> Card:
        return self.cards[idx]
    
    def pop(self, rand: bool=False) -> Card:
        """
        A wrapper for list.pop(), normally O(1), but
        if rand is True evaluates to O(n)
        :param rand: Whether to choose a random element to pop
        :return: A card from the deck 
        """
        if rand:
            return self.cards.pop(int(random.uniform(0, len(self.cards))))
        return self.cards.pop()

    def shuffle(self) -> None:
        """
        Shuffle deck using random.shuffle as it utilizes Fisher-Yates
        O(n)
        :return: None
        """
        random.shuffle(self.cards)

    def push(self, discards: List[Card]=None) -> None:
        """
        Push cards back to bottom of deck in O(n*c) where c is number of discards
        :param discards: Discarded cards to be added to bottom of deck
        :return: None
        """
        if discards:
            for card in discards:
                self.cards.insert(0, card)
