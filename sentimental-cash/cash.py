# TODO
from cs50 import get_float


def main():
    while True:
        cents = get_float("Change Owed: ")
        if cents >= 0:
            break
    quarters = int(get_quarter(cents))
    cents = round(cents - quarters * 0.25, 2)
    dimes = int(get_dime(cents))
    cents = round(cents - dimes * 0.1, 2)
    nickels = int(get_nickel(cents))
    cents = round(cents - nickels * 0.05, 2)
    pennies = int(get_pennies(cents))
    answer = quarters + dimes + nickels + pennies
    print(f"{answer}")


def get_quarter(n):
    value = n / 0.25
    return value


def get_dime(n):
    value = n / 0.10
    return value


def get_nickel(n):
    value = n / 0.05
    return value


def get_pennies(n):
    value = n / 0.01
    return value


main()

