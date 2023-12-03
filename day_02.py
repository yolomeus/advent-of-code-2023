from utils import read_file_as_lines

# number of
cubes = {'red': 12,
         'green': 13,
         'blue': 14}


def parse_draws(turn: str):
    draws = turn.split(',')
    return {color: int(i) for i, color in map(lambda x: x.split(), draws)}


def parse_game(line: str):
    game_title, game_data = line.split(':')
    game_id = int(game_title.split()[-1])
    turns = game_data.split(';')
    game = [parse_draws(turn) for turn in turns]
    return {'id': game_id, 'game': game}


def is_possible_draw(draw):
    return all(draw[color] <= cubes[color] for color in draw)


def is_possible_game(game):
    return all([is_possible_draw(draw) for draw in game])


def main():
    lines = read_file_as_lines('data/day_02.txt')
    games = tuple(map(parse_game, lines))
    is_valid_game = tuple(map(lambda x: is_possible_game(x['game']), games))
    valid_game_ids = [game['id'] for game, is_valid in zip(games, is_valid_game)
                      if is_valid]

    print(sum(valid_game_ids))


if __name__ == '__main__':
    main()
