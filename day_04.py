from utils import read_file_as_lines


def parse_list(number_string: str) -> list[int]:
    return list(map(int, number_string.split()))


def parse_line(line: str) -> tuple[list[int], list[int]]:
    cards = line.split(':')[1]
    winning_nums, actual_nums = cards.split('|')
    return parse_list(winning_nums), parse_list(actual_nums)


def main():
    data = read_file_as_lines('data/day_04.txt')
    total = 0
    for winning_nums, actual_nums in map(parse_line, data):
        points = 0
        for winning_num in winning_nums:
            if winning_num in actual_nums:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        total += points

    print('part 1:', total)


if __name__ == '__main__':
    main()
