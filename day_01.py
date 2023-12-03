from typing import List

from utils import read_file_as_lines


# part one
def cat_first_and_last_num(text: str) -> int:
    nums = []
    for c in text:
        try:
            x = int(c)
            nums.append(x)
        except ValueError:
            pass

    return int(str(nums[0]) + str(nums[-1]))


def get_sum_numbers(data: List[str], get_number_fn):
    total = 0
    for text in data:
        total += get_number_fn(text)

    return total


# part two
number_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
number_to_value = {text: i + 1 for i, text in enumerate(number_strings)}


def get_first_number(text):
    number_buffer = ""
    first = None
    found_num = False
    for c in text:
        if c.isdigit():
            first = c
            break

        number_buffer += c
        for num in number_strings:
            if num in number_buffer:
                first = number_to_value[num]
                found_num = True
                break

        if found_num:
            break

    return first


def get_last_number(text):
    number_buffer = ""
    last = None
    found_num = False

    for c in reversed(text):
        if c.isdigit():
            last = c
            break

        number_buffer = c + number_buffer
        for num in number_strings:
            if num in number_buffer:
                last = number_to_value[num]
                found_num = True
                break

        if found_num:
            break

    return last


def cat_first_and_last_num_or_str(text: str) -> int:
    return int(f"{get_first_number(text)}{get_last_number(text)}")


def main():
    data = read_file_as_lines('data/day_01.txt')
    print("part 1:", get_sum_numbers(data, cat_first_and_last_num))
    print("part 2:", get_sum_numbers(data, cat_first_and_last_num_or_str))


if __name__ == '__main__':
    main()
