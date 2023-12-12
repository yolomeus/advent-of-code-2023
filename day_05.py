from functools import partial

from utils import read_file


def parse_mapping(mapping_str: str):
    dest, src, length = map(int, mapping_str.split())
    return {'src_range': range(src, src + length), 'dest': dest}


def parse_map(map_str: str):
    mappings = map_str[1:].split('\n')
    mappings = list(map(parse_mapping, mappings))
    return mappings


def parse_data(data: str):
    data = data.strip().split('\n\n')
    seeds, maps = data[0], data[1:]

    seeds = seeds.split(':')[1].split()
    seeds = list(map(int, seeds))

    maps = [x.split(':')[1] for x in maps]
    maps = list(map(parse_map, maps))
    return seeds, maps


def get_location_number(seed, maps):
    next_value = seed
    for map_ in maps:
        for map_item in map_:
            src_range = map_item['src_range']
            if next_value in src_range:
                next_value = map_item['dest'] + next_value - src_range[0]
                break

    return next_value


def shift_num(num: int, src_range: range, dest: int):
    return num - src_range.start + dest


def shift_range(range_: range, src_range: range, dest: int):
    return range(shift_num(range_.start, src_range, dest),
                 shift_num(range_.stop, src_range, dest))


def split_range(map_: list[dict[str, range]], range_: range):
    ranges = []
    new_range_queue = [range_]

    while len(new_range_queue) > 0:
        new_range = new_range_queue.pop(0)
        found_match = False
        for map_item in map_:
            src_range, dest = map_item['src_range'], map_item['dest']
            if new_range.start in src_range:
                found_match = True
                if new_range.stop > src_range.stop:
                    ranges.append(range(new_range.start, src_range.stop))
                    new_range_queue.append(range(src_range.stop, new_range.stop))
                else:
                    ranges.append(new_range)

        if not found_match:
            ranges.append(new_range)

    return ranges


def map_range(range_: range, map_: list[dict[str, range]]) -> list[range]:
    mapped_ranges = []
    # split range based on maps if too large
    sub_ranges = split_range(map_, range_)
    for sub_range in sub_ranges:
        shifted = False
        for mapping in map_:
            src_range, dest = mapping['src_range'], mapping['dest']
            if sub_range.start in src_range:
                mapped_ranges.append(shift_range(sub_range, src_range, dest))
                shifted = True
                break

        # any range that we did not shift maps to itself
        if not shifted:
            mapped_ranges.append(sub_range)

    return mapped_ranges


def main():
    data = read_file('data/day_05.txt')
    seeds, maps = parse_data(data)

    location_numbers = list(map(partial(get_location_number, maps=maps), seeds))
    print('part 1 :', min(location_numbers))

    ranges = (range(x, x + y) for x, y in zip(seeds[0::2], seeds[1::2]))
    for map_ in maps:
        ranges = [map_range(range_, map_) for range_ in ranges]
        # flatten
        ranges = [y for x in ranges for y in x]

    # we can easily get the min of a range by selecting its lower bound
    print('part 2 :', min(range_.start for range_ in ranges))


if __name__ == '__main__':
    main()
