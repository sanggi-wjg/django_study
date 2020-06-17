class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    BACK_RED = '\033[41m'


# print_to_server = lambda color, msg, *args: print(color, msg, *args, Colors.ENDC)

def print_green(msg, *args):
    print(Colors.OKGREEN, msg, *args, Colors.ENDC)


def print_yellow(msg, *args):
    print(Colors.WARNING, msg, *args, Colors.ENDC)


def print_red(msg, *args):
    print(Colors.FAIL, msg, *args, Colors.ENDC)


def print_back_red(msg, *args):
    print(Colors.BACK_RED, msg, *args, Colors.ENDC)
