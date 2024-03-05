import random


def get_random_coordinate(w_size):
    x = random.randint(0, w_size['width'])
    y = random.randint(0, w_size['height'])
    return x, y
