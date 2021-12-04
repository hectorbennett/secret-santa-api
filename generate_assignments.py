import random


def generate_assignments(santas, invalid_pairs=None):
    max_attempts = 200
    while max_attempts:
        max_attempts -= 1
        santa_dicts = assign_random_giftees(santas)
        if not is_derangement(santa_dicts):
            continue
        if has_invalid_pairs(santa_dicts, invalid_pairs):
            continue
        return santa_dicts

def assign_random_giftees(santa_list):
    """
    Creates a randomised list of pairs from a list of names.
    """
    giftee_list = [santa['santa'] for santa in santa_list]
    random.shuffle(giftee_list)
    for i, giftee in enumerate(giftee_list):
        santa_list[i]['giftee'] = giftee
    return santa_list

def is_derangement(dict_list):
    """
    Checks if a list of 2-tuples is a derangement, that is, no santa is paired
    with themselves.
    """
    for santa_dict in dict_list:
        if santa_dict['santa'] == santa_dict['giftee']:
            return False
    return True

def has_invalid_pairs(dict_list, invalid_pairs):
    if not invalid_pairs:
        return
    for santa_dict in dict_list:
        for invalid_pair in invalid_pairs:
            if santa_dict['santa'] in invalid_pair and santa_dict['giftee'] in invalid_pair:
                return True
    return False
