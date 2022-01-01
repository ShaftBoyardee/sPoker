from deck import Card, Deck
from hand import Hand, Player
from typing import  TypeVar, List, Union, Tuple
import itertools

T = TypeVar("T")
Holdem = TypeVar("Holdem")

class Holdem:
    """All game functions of Texas Hold 'Em"""
    def __init__(self) -> None:
        self.community = Hand()
        self.players = list()
        self.deck = Deck()
        self.deck.shuffle()
    
    def _deal(self, player: Player) -> None:
        """Deal a card to a player"""
        player.deal(self.deck.pop())
    
    def _gen_possible_hands(self, hand: Hand) -> List[Hand]:
        """
        Generate all possible hands from player's cards and community
        """
        if len(self.community) <= 3:
            return Hand(card_list=hand.cards + self.community)
        return [Hand(card_list=(hand.cards + list(comb))) for comb in list(itertools.combinations(self.community.cards, 3))]
    
    def _check_flush(self, hand: Hand) -> bool:
        """
        Check for a flush (all same suit)
        :param hand: Hand to check
        :return: If hand has a flush or not
        """
        hand.sort_suit()
        if hand[0].suit == hand[-1].suit:
            return True
        return False
    
    def _check_straight(self, hand: Hand) -> Union[bool, bool, bool]:
        """
        Check for a straight (ascending ranks for all 5)
        :param hand: Hand to check
        :return: if hand has a straight, if flush, if royal
        """
        # Aces cases
        flush = self._check_flush(hand)
        hand.sort_rank()
        if hand[-1].value == 14:
            if hand[0].value == 2 and hand[1].value == 3 and \
            hand[2].value == 4 and hand[3].value == 5:
                # steel wheel
                return True, flush, False
            elif hand[0].value == 10 and hand[1].value == 11 and \
            hand[2].value == 12 and hand[3].value == 13:
                # royal straight
                return True, flush, True
        else:
            last = hand[0].value - 1
            for card in hand:
                if card.value != last + 1:
                    return False, flush, False
            return True, flush, False

    def _check_4(self, hand: Hand) -> Union[bool, int]:
        """
        Check for 4 of a kind
        :param hand: Hand to check
        :return: If 4 of a kind and card value
        """
        hand.sort_rank()
        if (hand[0] == hand[1] == hand[2] \
        == hand[3]) or (hand[1] == hand[2] \
        == hand[3] == hand[4]):
            return True, hand[1].value
        return False, None
    
    def _check_full_house(self, hand: Hand) -> Union[bool, int, int]:
        """
        Check for full house
        :param hand: Hand to check
        :return: If full house, 3 of a kind card val, pair card val
        """
        hand.sort_rank()
        if (hand[0] == hand[1] == hand[2]) and \
           (hand[3] == hand[4]):
           return True, hand[0].value, hand[3].value
        elif (hand[2] == hand[3] == hand[4]) and \
            (hand[0] == hand[1]):
           return True, hand[2].value, hand[0].value
        return False, None, None
    
    def _check_3(self, hand: Hand) -> Union[bool, int]:
        """
        Check for 3 of a kind
        :param hand: Hand to check
        :return: If 3 of a kind and card value
        """
        hand.sort_rank()
        if (hand[0] == hand[1] == hand[2]) or \
        (hand[1] == hand[2] == hand[3]) or \
        (hand[2] == hand[3] == hand[4]):
            return True, hand[2].value
        return False, None
    
    def _check_2_pair(self, hand: Hand) -> Union[bool, int, int]:
        """
        Check for 2 pair
        :param hand: Hand to check
        :return: If 2 pair, first pair val, second pair val
        """
        hand.sort_rank()
        if (hand[0] == hand[1]) or (hand[1] == hand[2]):
            if (hand[2] == hand[3]) or (hand[3] == hand[4]):
                return True, hand[1].value, hand[3].value
        return False, None, None

    def _check_pair(self, hand: Hand) -> Union[bool, int]:
        """
        Check single pair
        :param hand: Hand to check
        :return: If pair, pair val
        """
        hand.sort_rank()
        if hand[0] == hand[1]:
            return True, hand[0].value
        elif hand[1] == hand[2]:
            return True, hand[1].value
        elif hand[2] == hand[3]:
            return True, hand[2].value
        elif hand[3] == hand[4]:
            return True, hand[3].value
        return False, None
    
    def _get_high_card(self, hand: Hand) -> Card:
        return max(hand)

    def _assess_hand(self, hand: Hand) -> dict:
        """
        Assess the hand using scoring methods
        :param hand: The hand to score
        :return: Dictionary of hand information
        """
        hand_data = dict()
        high_card = self._get_high_card(hand)
        straight, flush, royal = self._check_straight(hand)
        hand_data["flush"] = flush
        if straight:
            hand_data["type"] = 8
            hand_data["royal"] = royal
            hand_data["high_card"] = high_card
            return hand_data
        four, rank = self._check_4(hand)
        if four:
            hand_data["type"] = 7
            hand_data["rank"] = rank
            return hand_data
        full, rank_1, rank_2 = self._check_full_house(hand)
        if full:
            hand_data["type"] = 6
            hand_data["rank1"] = rank_1
            hand_data["rank2"] = rank_2
            return hand_data
        if flush:
            hand_data["type"] = 5
            hand_data["high_card"] = flush
            return hand_data
        three, rank = self._check_3(hand)
        if three:
            hand_data["type"] = 4
            hand_data["rank"] = rank
            return hand_data
        two_pair, rank_1, rank_2 = self._check_2_pair(hand)
        if two_pair:
            hand_data["type"] = 3
            hand_data["rank1"] = rank_1
            hand_data["rank2"] = rank_2
            hand_data["high_card"] = self._get_high_card(hand)
            return hand_data
        pair, rank = self._check_pair(hand)
        if pair:
            hand_data["type"] = 2
            hand_data["rank"] = rank
            hand_data["high_card"] = high_card
            return hand_data
        hand_data["type"] = 1
        hand_data["high_card"] = high_card
        return hand_data
    
    def _compare_hands(self, data_1: dict, data_2: dict) -> bool:
        if data_1["type"] > data_2["type"]:
            return True
        elif data_1["type"] == data_2["type"]:
            if (data_1.get("rank") and data_1.get("rank") > data_2.get("rank")) or \
            (data_1.get("rank1") and data_1.get("rank1") > data_2.get("rank1")) or \
            (data_1.get("royal") and not data_2.get("royal")) or \
            (data_1.get("high_card") and data_1.get("high_card") > data_2.get("high_card")):
                return True
        return False

    def _assign_best_hand(self, player: Player) -> None:
        """
        Find possible hands and assign the highest value hand
        to the player
        :param player: Player object to get hands for and assign 
        a best hand to
        :return: none
        """
        possible = self._gen_possible_hands(player.hand)
        best_data = {"type": 0}
        best_hand: Hand = Hand()
        for hand in possible:
            hand_data = self._assess_hand(hand)
            if self._compare_hands(hand_data, best_data):
                best_hand = hand
                best_data = hand_data
        best_data["hand"] = best_hand
        player.best_hand = best_data



# Test it!

# Below is an example of setup and play of Hold 'Em poker. These will likely become methods
# as development continues.

type_descriptors = {"8": "straight", "7": "4 of a kind", "6": "full house", "5": "flush",
                    "4": "3 of a kind", "3": "two pair", "2": "pair", "1": "high card"}
    

player1 = Player(holdem=True)
dealer = Player("dealer", True)
game = Holdem()
game.players.append(player1)
game.players.append(dealer)

# setup
for _ in range(2):
    for player in game.players:
        game._deal(player)
for player in game.players:
    print(player)

# round 1
game.community.deal(3, game.deck)
print("flop: " + str(game.community))

# round 2
game.community.deal(1, game.deck)
print("turn: " + str(game.community))

# round 3
game.community.deal(1, game.deck)
print("river: " + str(game.community))

for player in game.players:
    game._assign_best_hand(player)
    print(player.alias + "'s hand: " + str(player.best_hand["hand"]))

player1_hand = game.players[0].best_hand
dealer_hand = game.players[1].best_hand
better = game._compare_hands(player1_hand, dealer_hand)
if better:
    print("player won with: " + type_descriptors[str(player1_hand["type"])])
else:
    print("dealer won with: " + type_descriptors[str(dealer_hand["type"])])