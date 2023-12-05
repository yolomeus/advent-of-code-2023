from typing import Dict, Iterable

from utils import read_file_as_lines

Position = tuple[int, int]
Matrix = Dict[Position, str]


def parse_to_matrix(data: list[str]) -> Matrix:
    return {(i, j): symbol
            for i, line in enumerate(data)
            for j, symbol in enumerate(line)}


def adj_positions(position: Position) -> list[Position]:
    i, j = position
    # hardcoded because I don't want to think about it
    return [(i, j + 1),
            (i, j - 1),
            (i + 1, j),
            (i - 1, j),
            (i + 1, j + 1),
            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 1, j - 1)]


def is_symbol(position: Position, matrix: Matrix) -> bool:
    i, j = position
    c = matrix.get((i, j), '.')
    return not c.isdigit() and c != '.'


def is_adjacent_to_symbol(position: Position, matrix: Matrix) -> bool:
    return any([is_symbol(pos, matrix) for pos in adj_positions(position)])


def is_part_number(positions: Iterable[Position], matrix: Matrix) -> bool:
    """A number is a part number if any of its positions is adjacent to a symbol
    """
    return any(is_adjacent_to_symbol(position, matrix) for position in positions)


def get_nums_as_positions(matrix: Matrix) -> list[list[Position]]:
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


def positions_to_number(positions: Iterable[Position], matrix: Matrix) -> int:
    num = ''
    for pos in positions:
        num += matrix[pos]
    return int(num)


def get_star_positions(matrix: Matrix) -> list[Position]:
    return [pos for pos, c in matrix.items() if c == '*']


def main():
    data = read_file_as_lines('data/day_03.txt')
    matrix = parse_to_matrix(data)
    nums_as_positions = get_nums_as_positions(matrix)

    part_numbers = []
    for positions in nums_as_positions:
        if is_part_number(positions, matrix):
            part_numbers.append(positions_to_number(positions, matrix))

    print("part 1:", sum(part_numbers))

    total = 0
    for star_pos in get_star_positions(matrix):
        adj_nums = set()
        for adj_pos in adj_positions(star_pos):
            if matrix[adj_pos].isdigit():
                for num_positions in nums_as_positions:
                    if adj_pos in num_positions:
                        adj_nums.add(tuple(num_positions))
                    if len(adj_nums) > 2:
                        break

        if len(adj_nums) == 2:
            adj_nums = list(adj_nums)
            total += positions_to_number(adj_nums[0], matrix) * positions_to_number(adj_nums[1], matrix)

    print("part 2:", total)


if __name__ == '__main__':
    main()
