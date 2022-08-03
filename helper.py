import re


def get_int_input_between_range(min_int, max_int):
    options = str(min_int)
    if min_int != max_int:
        options = f'Any integer between {min_int} and {max_int}'
    print(f'Options:  {options}')
    user_choice = int_input()
    while not int_between_range(user_choice, min_int, max_int):
        user_choice = int_input()
    return user_choice


def specify_options_for_range(min_int: int = None, max_int: int = None):
    options = "Enter integer(s)"
    if min_int is not None and max_int is not None:
        if min_int == max_int:
            options += f" {min_int}"
        else:
            options += f" equal to or greater than {min_int} and equal to or less than {max_int}"
    elif min_int is None and max_int is not None:
        options += f" equal to or less than {max_int}: "
    elif min_int is not None and max_int is None:
        options += f" equal to or greater than {min_int}: "
    elif min_int is None and max_int is None:
        options += ": "
    return options


def int_input(user_int: int = None):
    while type(user_int) != int:
        try:
            user_int = int(input('Enter an integer: '))
        except (TypeError, ValueError):
            print('Not a valid integer. An integer is a whole number. (e.g. 1, 42, 69 etc.)')
    return user_int


def keep_numbers_only(string_input):
    return re.sub("[^0-9^ ]", "", string_input)  # removes all characters that aren't numerical or spaces


def get_multiple_input_between_range(min_int, max_int):
    # This function can probably be refactored
    chosen_numbers = input(f'For multiple cards separate your choices spaces e.g. \'1 3\'\n'
                           f'Integers outside of the range will be ignored.\n'
                           f'{specify_options_for_range(min_int, max_int)}: ')
    chosen_indexes = set()
    temp_index = keep_numbers_only(chosen_numbers).strip()
    if temp_index == "":
        print(f'No integer input found. Try again.')
        return get_multiple_input_between_range(min_int, max_int)
    for each_string in temp_index.split():
        if int_between_range(int(each_string), min_int, max_int):
            chosen_indexes.add(int(each_string))
        else:
            print(f'Invalid input. {each_string} is out of the range.')
            return get_multiple_input_between_range(min_int, max_int)
    return list(chosen_indexes)


def int_between_range(check_int: int, min_int: int, max_int: int):
    return min_int <= check_int <= max_int
