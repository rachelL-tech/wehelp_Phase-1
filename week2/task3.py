def func3(index: int) -> None:
    base = [25, 23, 20, 21]
    quotient = index // 4
    remainder = index % 4
    answer = base[remainder] + (-2) * quotient
    print(answer)