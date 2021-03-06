import random

COLOR = {
    "PURPLE": '\033[95m',
    "CYAN": '\033[96m',
    "DARKCYAN": '\033[36m',
    "BLUE": '\033[94m',
    "GREEN": '\033[92m',
    "YELLOW": '\033[93m',
    "RED": '\033[91m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m',
    "END": '\033[0m'
}

RAND_COLOR = {
    "PURPLE": '\033[95m',
    "CYAN": '\033[96m',
    "DARKCYAN": '\033[36m',
    "BLUE": '\033[94m',
    "YELLOW": '\033[93m',
    "RED": '\033[91m'
}


def print_color(string, color=None):
    if color == "green":
        print(f'{COLOR["GREEN"]}{string}{COLOR["END"]}')
    elif color == "cyan":
        print(f'{COLOR["CYAN"]}{string}{COLOR["END"]}')
    elif color == "red":
        print(f'{COLOR["RED"]}{string}{COLOR["END"]}')
    elif color == "yellow":
        print(f'{COLOR["YELLOW"]}{string}{COLOR["END"]}')
    elif color == "blue":
        print(f'{COLOR["BLUE"]}{string}{COLOR["END"]}')
    elif color == "purple":
        print(f'{COLOR["PURPLE"]}{string}{COLOR["END"]}')
    elif color == "random":
        print(f'{RAND_COLOR[random.choice(list(RAND_COLOR.keys()))]}{string}{COLOR["END"]}')
    else:
        print(string)


def format_string(string, color=None):
    if color == "green":
        return f'{COLOR["GREEN"]}{string}{COLOR["END"]}'
    elif color == "cyan":
        return f'{COLOR["CYAN"]}{string}{COLOR["END"]}'
    elif color == "red":
        return f'{COLOR["RED"]}{string}{COLOR["END"]}'
    elif color == "yellow":
        return f'{COLOR["YELLOW"]}{string}{COLOR["END"]}'
    elif color == "blue":
        return f'{COLOR["BLUE"]}{string}{COLOR["END"]}'
    elif color == "purple":
        return f'{COLOR["PURPLE"]}{string}{COLOR["END"]}'
    elif color == "random":
        return f'{RAND_COLOR[random.choice(list(RAND_COLOR.keys()))]}{string}{COLOR["END"]}'
    else:
        return string