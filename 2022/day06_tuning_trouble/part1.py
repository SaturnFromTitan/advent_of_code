

def main():
    with open("input.txt") as f:
        buffer = f.read().strip()

    idx = 0
    length = 4
    for idx in range(len(buffer)):
        sub_buffer = buffer[idx:idx + length]
        unique_chars = set(sub_buffer)
        if len(unique_chars) == length:
            break
    answer = idx + length

    print(f"THE ANSWER IS: {answer}")


if __name__ == '__main__':
    main()
