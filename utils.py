from typing import List


def read_file_as_lines(filepath: str) -> List[str]:
    with open(filepath, 'r', encoding='utf-8') as fp:
        return list(map(lambda x: x.strip(), fp.readlines()))


def read_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as fp:
        return fp.read()
