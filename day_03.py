from typing import Dict, Iterable

from utils import read_file_as_lines

Position = tuple[int, int]
Matrix = Dict[Position, str]


def parse_to_matrix(data: list[str]) -> Matrix:
    return {(i, j): symbol
            for i, line in enumerate(data)
            for j, symbol in enumerate(line)}


def is_symbol(position: Position, matrix: Matrix) -> bool:
    i, j = position
    c = matrix.get((i, j), '.')
    return not c.isdigit() and c != '.'


def is_adjacent_to_symbol(position: Position, matrix: Matrix) -> bool:
    i, j = position
    # hardcoded because I don't want to think about it
    positions_to_check = [(i, j + 1),
                          (i, j - 1),
                          (i + 1, j),
                          (i - 1, j),
                          (i + 1, j + 1),
                          (i - 1, j - 1),
                          (i - 1, j + 1),
                          (i + 1, j - 1)]

    return any([is_symbol(pos, matrix) for pos in positions_to_check])


def is_part_number(positions: Iterable[Position], matrix: Matrix) -> bool:
    """A number is a part number if any of its positions is adjacent to a symbol
    """
    return any(is_adjacent_to_symbol(position, matrix) for position in positions)


def get_nums_as_positions(matrix) -> list[list[Position]]:
    """Represent each n-digit number as a set of positions in the matrix
    """
    number_positions = []
    current_digit_positions = []
    for pos in sorted(matrix):
        symbol = matrix[pos]

        if symbol.isdigit():
            current_digit_positions.append(pos)
        else:
            # the number is complete, clear the buffer
            if len(current_digit_positions) > 0:
                number_positions.append(current_digit_positions)
                current_digit_positions = []

    return number_positions


def positions_to_number(positions, matrix):
    num = ''
    for pos in positions:
        num += matrix[pos]
    return int(num)


def main():
    data = read_file_as_lines('data/day_03.txt')
    matrix = parse_to_matrix(data)
    nums_as_positions = get_nums_as_positions(matrix)

    part_numbers = []
    for positions in nums_as_positions:
        if is_part_number(positions, matrix):
            part_numbers.append(positions_to_number(positions, matrix))

    print("part 1:", sum(part_numbers))


if __name__ == '__main__':
    main()
