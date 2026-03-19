# TODO
def main():
    while True:
        try:
            height = int(input("Height: "))
        except ValueError:
            main()
            return 1
        if (height > 0) and (height < 9):
            break
    for x in range (height):
        print(" " * int((height - 1) - x), end = "")
        print("#" * int(x + 1))

main()
