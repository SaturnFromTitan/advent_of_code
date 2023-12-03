

def main():
    with open("input.txt") as f:
        buffer = f.read().strip()

    idx = 0
    length = 14
    is_found = False
    for idx in range(len(buffer)):
        sub_buffer = buffer[idx:idx + length]
        unique_chars = set(sub_buffer)
        if len(unique_chars) == length:
            is_found = True
            break

    if is_found:
        answer = idx + length
        print(f"THE ANSWER IS: {answer}")
    else:
        print("Didn't find a a matching substring")


if __name__ == '__main__':
    main()
