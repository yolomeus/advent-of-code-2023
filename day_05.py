from functools import partial
from multiprocessing import Pool

from tqdm import tqdm

from utils import read_file


def parse_mapping(mapping_str):
    dest, src, length = map(int, mapping_str.split())
    return {'src_range': range(src, src + length), 'dest': dest}


def parse_map(map_str: str):
    mappings = map_str[1:].split('\n')
    mappings = list(map(parse_mapping, mappings))
    return mappings


def parse_data(data):
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
        for mappings in map_:
            src_range = mappings['src_range']
            if next_value in src_range:
                next_value = mappings['dest'] + next_value - src_range[0]
                break

    return next_value


def main():
    data = read_file('data/day_05.txt')
    seeds, maps = parse_data(data)

    location_numbers = list(map(partial(get_location_number, maps=maps), seeds))
    print(min(location_numbers))

    # brute force for the giggles (takes 15min on my machine...)
    seeds = (range(x, x + y) for x, y in zip(seeds[0::2], seeds[1::2]))
    seeds = tuple(y for x in tqdm(seeds) for y in x)

    with Pool(12) as p:
        location_numbers = (num for num in
                            tqdm(p.imap_unordered(partial(get_location_number, maps=maps),
                                                  seeds,
                                                  chunksize=4096),
                                 total=len(seeds))
                            )
        print(min(location_numbers))


if __name__ == '__main__':
    main()
