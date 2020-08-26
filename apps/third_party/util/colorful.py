# print_to_server = lambda color, msg, *args: print(color, msg, *args, Colors.ENDC)
from apps.third_party.util.constants import Colors


def print_green(msg, *args):
    print(Colors.OKGREEN, msg, *args, Colors.ENDC)


def print_yellow(msg, *args):
    print(Colors.WARNING, msg, *args, Colors.ENDC)


def print_red(msg, *args):
    print(Colors.FAIL, msg, *args, Colors.ENDC)


def print_back_red(msg, *args):
    print(Colors.BACK_RED, msg, *args, Colors.ENDC)
