import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py <database> <sequence>")

    # TODO: Read database file into a variable
    csv1 = sys.argv[1]
    substr = []
    buffer = []
    with open(csv1, "r") as database:
        database_reader = csv.reader(database)
        for strname in database_reader:
            substr.append(strname[1:])
            break
        for data in database_reader:
            buffer.append(data)
    # print(f"line 20 {substr}")

    # TODO: Read DNA sequence file into a variable
    csv2 = sys.argv[2]
    with open(csv2, "r") as sequence:
        sequence_reader = sequence.readline()
        # print(f"{sequence_reader}")
    # TODO: Find longest match of each STR in DNA sequence
    subsequence = substr[0]
    # each of the longest str in dna sequence
    longest_str = []

    for STR in subsequence:
        # print(f"line 44{STR}")
        # print(f"line 45{sequence_reader}")
        longest_str.append(longest_match(sequence_reader, STR))
        # print(f"line 47{longest_str}")

    # TODO: Check database for matching profiles
    for check in buffer:
        # print(f"line 53 {check[1:]}")
        converted = [eval(i) for i in check[1:]]
        # print(f"line 55 {converted}")
        if longest_str == converted:
            print(f"{check[0]}")
            return 0

    print("No match")
    return 0


def longest_match(sequence, subsequence):  # sequence = whole string of DNA sequence, subsequence = STR
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)
    # print(f"{sequence}")
    # print(f"{sequence_length}")
    # print(f"{subsequence_length}")

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
