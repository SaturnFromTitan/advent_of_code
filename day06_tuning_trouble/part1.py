

def main():
    with open("input.txt") as f:
        buffer = f.read().strip()

    idx = 0
    for idx in range(len(buffer)):
        sub_buffer = buffer[idx:idx + 4]
        unique_chars = set(sub_buffer)
        if len(unique_chars) == 4:
            break
    answer = idx + 4

    print(f"THE ANSWER IS: {answer}")


if __name__ == '__main__':
    main()
