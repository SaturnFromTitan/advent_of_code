import collections
import dataclasses
from pathlib import Path

FILE_NAME = Path("input.txt")

CardValuesType = tuple[int, int, int, int, int]
HandTuplesType = tuple[int, int, int, int, int, int]

JOKER_SYMBOL = "J"
SYMBOLS = [JOKER_SYMBOL, "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
SYMBOL_VALUES = {symbol: idx for (idx, symbol) in enumerate(SYMBOLS, start=1)}


@dataclasses.dataclass
class Hand:
    type_value: int
    card_values: CardValuesType
    _symbols: str

    def to_tuple(self) -> HandTuplesType:
        return (self.type_value,) + self.card_values  # noqa: RUF005

    def __gt__(self, other: "Hand") -> bool:
        return self.to_tuple() > other.to_tuple()

    def __lt__(self, other: "Hand") -> bool:
        return self.to_tuple() < other.to_tuple()

    @classmethod
    def from_symbols(cls, symbols: str) -> "Hand":
        return cls(
            _symbols=symbols,
            type_value=cls._get_type_value(symbols),
            card_values=cls._get_symbol_values(symbols),
        )

    @staticmethod
    def _get_type_value(hand_with_jokers: str) -> int:  # noqa: PLR0911
        hand = Hand._convert_jokers(hand_with_jokers)

        counts = sorted(collections.Counter(hand).values(), reverse=True)
        highest_count = counts[0]
        if len(counts) == 1:
            second_highest_count = 0
        else:
            second_highest_count = counts[1]

        match (highest_count, second_highest_count):
            case (5, 0):
                return 7
            case (4, 1):
                return 6
            case (3, 2):
                return 5
            case (3, _):
                return 4
            case (2, 2):
                return 3
            case (2, _):
                return 2
            case _:
                return 1

    @staticmethod
    def _convert_jokers(hand_with_jokers: str) -> str:
        counter = collections.Counter(hand_with_jokers)
        if counter[JOKER_SYMBOL] == len(hand_with_jokers):
            return hand_with_jokers

        # now there's at least one non-joker card
        highest_count = max(
            [count for (symbol, count) in counter.items() if symbol != JOKER_SYMBOL]
        )
        best_symbols_by_count = [
            symbol
            for (symbol, count) in counter.items()
            if count == highest_count and symbol != JOKER_SYMBOL
        ]
        best_symbol = sorted(
            best_symbols_by_count, key=lambda s: SYMBOL_VALUES[s], reverse=True
        )[0]
        return hand_with_jokers.replace(JOKER_SYMBOL, best_symbol)

    @staticmethod
    def _get_symbol_values(hand: str) -> CardValuesType:
        return tuple(SYMBOL_VALUES[symbol] for symbol in hand)  # type: ignore[return-value]


def main() -> None:
    with open(FILE_NAME) as f:
        hand_bids = parse_file(f)

    answer = 0
    sorted_hand_bids = sorted(hand_bids, key=lambda hb: hb[0])
    for idx, (_, bid) in enumerate(sorted_hand_bids, start=1):
        answer += idx * bid
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[tuple[Hand, int]]:
    results = []
    for line in f.readlines():
        hand_raw, bid = line.strip().split()
        hand = Hand.from_symbols(hand_raw)
        results.append((hand, int(bid)))
    return results


if __name__ == "__main__":
    # test cases
    assert Hand.from_symbols("AAAAA").type_value == 7
    assert Hand.from_symbols("AA8AA").type_value == 6
    assert Hand.from_symbols("23332").type_value == 5
    assert Hand.from_symbols("TTT98").type_value == 4
    assert Hand.from_symbols("23432").type_value == 3
    assert Hand.from_symbols("A23A4").type_value == 2
    assert Hand.from_symbols("23456").type_value == 1

    # with jokers
    assert Hand.from_symbols("32T3K").type_value == 2
    assert Hand.from_symbols("T55J5").type_value == 6
    assert Hand.from_symbols("KK677").type_value == 3
    assert Hand.from_symbols("KTJJT").type_value == 6
    assert Hand.from_symbols("QQQJA").type_value == 6
    assert Hand.from_symbols("22222") > Hand.from_symbols("JJJJJ")
    assert Hand.from_symbols("22222") > Hand.from_symbols("J2222")
    assert Hand.from_symbols("22222") > Hand.from_symbols("2222J")
    assert Hand.from_symbols("32222") < Hand.from_symbols("JJJJ2")

    main()
