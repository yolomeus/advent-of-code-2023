from utils import read_file_as_lines


def parse_list(number_string: str) -> list[int]:
    return list(map(int, number_string.split()))


def parse_line(line: str):
    idx, cards = line.split(':')
    idx = int(idx.split()[-1])
    winning_nums, actual_nums = cards.split('|')
    return idx, (parse_list(winning_nums), parse_list(actual_nums))


def get_num_winners(card):
    winning_nums, actual_nums = card
    return len([num for num in winning_nums if num in actual_nums])


def main():
    data = read_file_as_lines('data/day_04.txt')
    indices, cards = zip(*list(map(parse_line, data)))
    total = 0
    for winning_nums, actual_nums in cards:
        points = 0
        for winning_num in winning_nums:
            if winning_num in actual_nums:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        total += points

    print('part 1:', total)

    id_to_card = dict(zip(indices, cards))
    id_to_winners = {i: get_num_winners(card) for i, card in id_to_card.items()}

    id_to_num_cards = {i: 1 for i, _ in id_to_card.items()}

    for idx in id_to_num_cards:
        for _ in range(id_to_num_cards[idx]):
            num_winners = id_to_winners[idx]
            for k in range(1, num_winners + 1):
                id_to_num_cards[idx + k] += 1

    print('part 2:', sum(id_to_num_cards.values()))


if __name__ == '__main__':
    main()
