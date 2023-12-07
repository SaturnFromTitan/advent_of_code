import collections
import dataclasses
from pathlib import Path

FILE_NAME = Path("input.txt")

CardValuesType = tuple[int, int, int, int, int]
HandTuplesType = tuple[int, int, int, int, int, int]

CARD_SYMBOLS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
CARD_VALUES = {symbol: idx for (idx, symbol) in enumerate(CARD_SYMBOLS, start=1)}


@dataclasses.dataclass
class Hand:
    type_value: int
    card_values: CardValuesType
    _symbols: str

    def to_tuple(self) -> HandTuplesType:
        return (self.type_value,) + self.card_values  # noqa: RUF005

    @classmethod
    def from_symbols(cls, symbols: str) -> "Hand":
        return cls(
            _symbols=symbols,
            type_value=cls._get_type_value(symbols),
            card_values=cls._get_card_values(symbols),
        )

    @staticmethod
    def _get_type_value(hand: str) -> int:  # noqa: PLR0911
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
    def _get_card_values(hand: str) -> CardValuesType:
        return tuple(CARD_VALUES[symbol] for symbol in hand)  # type: ignore[return-value]


def main() -> None:
    with open(FILE_NAME) as f:
        hand_bids = parse_file(f)

    answer = 0
    sorted_hand_bids = sorted(hand_bids, key=lambda hb: hb[0].to_tuple())
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
    assert Hand.from_symbols("AAAAA").type_value == 7  # noqa: PLR2004
    assert Hand.from_symbols("AA8AA").type_value == 6  # noqa: PLR2004
    assert Hand.from_symbols("23332").type_value == 5  # noqa: PLR2004
    assert Hand.from_symbols("TTT98").type_value == 4  # noqa: PLR2004
    assert Hand.from_symbols("23432").type_value == 3  # noqa: PLR2004
    assert Hand.from_symbols("A23A4").type_value == 2  # noqa: PLR2004
    assert Hand.from_symbols("23456").type_value == 1

    main()
