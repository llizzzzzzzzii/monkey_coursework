import random


def scroll_to_random_position(page):
    width = page.evaluate('() => document.body.scrollWidth')
    height = page.evaluate('() => document.body.scrollHeight')

    random_x = random.randint(0, width)
    random_y = random.randint(0, height)

    page.evaluate('window.scrollTo({}, {})'.format(random_x, random_y))
