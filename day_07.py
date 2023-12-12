from collections import Counter
from dataclasses import dataclass

from utils import read_file_as_lines


def five_of_a_kind(hand: Counter):
    return 5 in hand.values()


def four_of_a_kind(hand: Counter):
    return 4 in hand.values()


def full_house(hand: Counter):
    return len(hand) == 2 and 3 in hand.values()


def three_of_a_kind(hand: Counter):
    return len(hand) == 3 and 3 in hand.values()


def two_pair(hand: Counter):
    return len(hand) == 3 and len([x for x in hand.values() if x == 2]) == 2


def one_pair(hand: Counter):
    return 2 in hand.values() and len([x for x in hand.values() if x != 2]) == 3


def high_card(hand: Counter):
    return len(hand) == 5


hand_types = [five_of_a_kind, four_of_a_kind, full_house, three_of_a_kind, two_pair, one_pair, high_card]
card_types = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_type_to_value = {card_type: i for i, card_type in enumerate(card_types)}


@dataclass
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.hand = Counter(cards)

        self.type_rank = None
        for i, type_fn in enumerate(hand_types):
            if type_fn(self.hand):
                self.type_rank = i
                break

    def __gt__(self, other):
        if self.type_rank == other.type_rank:
            for c0, c1 in zip(self.cards, other.cards):
                if c0 != c1:
                    return card_type_to_value[c0] < card_type_to_value[c1]

        return self.type_rank < other.type_rank


def parse_data(data):
    hands, bids = zip(*[x.split() for x in data])
    return [(Hand(cards), int(payout)) for cards, payout in zip(hands, bids)]


def main():
    data = read_file_as_lines('data/day_07.txt')
    card_to_bid = parse_data(data)
    card_to_bid = sorted(card_to_bid, key=lambda x: x[0])
    _, bids_sorted = zip(*card_to_bid)

    payout = 0
    for i, bid in enumerate(bids_sorted, start=1):
        payout += i * bid

    print(payout)


if __name__ == '__main__':
    main()
