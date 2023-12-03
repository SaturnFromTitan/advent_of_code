INPUT_FILE = "input.txt"


def main():
    with open(INPUT_FILE) as f:
        numbers = parse_file(f)

    decrypted_numbers = decrypt(numbers)
    answer = get_grove_coordinates(decrypted_numbers)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f):
    decryption_key = 811589153
    return [int(line.strip()) * decryption_key for line in f.readlines()]


def decrypt(numbers):
    indexes = list(range(len(numbers)))
    for _ in range(10):
        numbers, indexes = _decrypt(numbers, indexes)
    return numbers


def _decrypt(numbers, indexes):
    num_numbers = len(numbers)
    for original_index in range(num_numbers):
        current_index = indexes.index(original_index)
        value = numbers.pop(current_index)

        # since indexes '0' and '-1' should be treated equally, we
        # use mod (n - 1)
        # Note: this also works for negative numbers
        new_index = (current_index + value) % (num_numbers - 1)

        indexes.pop(current_index)
        indexes.insert(new_index, original_index)
        numbers.insert(new_index, value)
    return numbers, indexes


def get_grove_coordinates(numbers):
    zero_index = numbers.index(0)

    num_numbers = len(numbers)
    index1 = (zero_index + 1000) % num_numbers
    index2 = (zero_index + 2000) % num_numbers
    index3 = (zero_index + 3000) % num_numbers
    return numbers[index1] + numbers[index2] + numbers[index3]


if __name__ == '__main__':
    main()
