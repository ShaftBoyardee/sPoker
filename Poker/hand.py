from deck import Card, Deck
from typing import TypeVar, List

T = TypeVar("T")
Hand = TypeVar("Hand")
HandIter = TypeVar("HandIter")
Player = TypeVar("Player")

class HandIter:
    """Iterator for hand class"""
    def __init__(self, hand: Hand) -> None:
        self._hand = hand
        self._idx = 0
    
    def __next__(self):
        if self._idx < len(self._hand):
            self._idx += 1
            return self._hand[self._idx - 1]
        raise StopIteration
    

class Hand:
    """Playing card hand class"""
    def __init__(self, card_list: List[Card]=None) -> None:
        self.cards = list()
        if card_list:
            for card in card_list:
                self.cards.append(card)

    def __str__(self) -> str:
        out = str()
        for c in self.cards:
            out += str(c) + " "
        out = out.rstrip()
        return out
    
    def __getitem__(self, idx: int) -> Card:
        """Return card at index"""
        # should throw out of range anyway if not an index
        return self.cards[idx]
    
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __iter__(self) -> HandIter:
        return HandIter(self)

    def deal(self, num: int=1, deck: Deck=None, sequential: bool=True) -> None:
        """
        Deal a set number of cards from a deck
        :param num: Number of cards to deal
        :param deck: Deck to deal cards from
        :param sequential: If multiple, whether to deal cards one after another
        or simulate pulling randomly from deck
        """
        # will utilize deck list as stack unless sequential is false
        if deck:
            for i in range(num):
                self.cards.append(deck.pop(rand=not sequential))
        
    def add_card(self, card: Card) -> None:
        """
        Wrapper for adding a card externally from deck
        """
        self.cards.append(card)
    
    def sort_rank(self, descending=False) -> None:
        """
        Sort cards based on point value
        :param descending: whether ascending or descending order
        :return: None
        """
        self.cards.sort(key=lambda c: c.value, reverse=descending)
    
    def sort_suit(self) -> None:
        """
        Sort cards based on suit
        :return: None
        """
        SuitEnums = {"spades": 1, "clubs": 2, "hearts": 3, "diamonds": 4}
        # 5 will be no suit (joker) enum
        self.cards.sort(key=lambda c: SuitEnums[c.suit] if c.suit else 5, reverse=False)
    
    def discard(self, deck: Deck=None, all: bool=False, card: Card=None) -> None:
        """
        Discard cards and add back into a deck or permanently discard
        """
        discards = list()
        if all:
            while len(self.cards) > 0:
                discards.append(self.cards.pop())
        elif card:
            discards.append(card)
        if deck:
            deck.push(discards=discards)

class Player:
    """Player aka hand container"""
    def __init__(self, alias: str=None, holdem: bool=False, purse: int=0) -> None:
        self.hand = Hand()
        if holdem:
            self.best_hand = dict()
        self.purse = purse
        self.alias = alias or "Player"
    
    def __str__(self) -> str:
        return self.alias + "'s hand: " + str(self.hand)
    
    def __repr__(self) -> str:
        return str(self)
    
    def deal(self, card: Card) -> None:
        self.hand.add_card(card)