from functools import reduce

from utils import read_file_as_lines


def parse_line(line):
    return list(map(int, line.split(':')[1].split()))


def parse_line_no_spaces(line):
    return int(''.join(line.split(':')[1].split()))


def num_ways_to_win(time, distance):
    n_ways_to_win = 0
    for hold_button_secs in range(time):
        if (time - hold_button_secs) * hold_button_secs > distance:
            n_ways_to_win += 1

    return n_ways_to_win


def main():
    data = read_file_as_lines('data/day_06.txt')

    n_ways_per_game = []
    times = parse_line(data[0])
    distances = parse_line(data[1])
    for time, distance in zip(times, distances):
        n_ways_per_game.append(num_ways_to_win(time, distance))

    print('part 1:', reduce(lambda x, y: x * y, n_ways_per_game))

    single_time = parse_line_no_spaces(data[0])
    single_dist = parse_line_no_spaces(data[1])
    print('part 2:', num_ways_to_win(single_time, single_dist))


if __name__ == '__main__':
    main()
