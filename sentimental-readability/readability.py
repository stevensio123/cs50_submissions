# TODO
def main():
    text = input("Text: ")
    letters = count_letters(text)
    # print(f"{letters}")
    words = len(text.split())
    # print(f"{words}")
    sentences = count_sentences(text)
    # print(f"{sentences}")
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = (0.0588 * L) - (0.296 * S) - 15.8
    if round(index) < 1:
        print("Before Grade 1")
    elif round(index) > 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(index)}")
    return 0


def count_letters(txt):
    i = 0
    for char in txt:
        if char.isalpha():
            i += 1
    return i


def count_sentences(txt):
    period = txt.count(".")
    question = txt.count("?")
    exc = txt.count("!")
    value = period + question + exc
    return value


main()

