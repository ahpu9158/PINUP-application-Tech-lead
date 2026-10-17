"""
Problem 1 (Logic): simulate the BOX / LINE instruction program.
"""


def run(trace: bool = False) -> dict:
    box = {1: 860, 2: 15, 3: 1, 4: 1, 5: 3}
    answer = {}

    def double_jump(x: int, current_line: int) -> int:
        box[x] *= 2
        return current_line + x

    def line_3() -> int:
        box[2] = box[2] + box[5]
        return 7

    def line_4() -> int:
        answer["A"] = box[3]
        return 1

    def line_5() -> int:
        box[4] = box[4] + box[3]
        return 3

    def line_6() -> int:
        box[3] = box[3] + box[4]
        return 2

    def line_7() -> int:
        return 9 if box[2] > 100 else 8

    def line_8() -> int:
        return 4 if box[2] > 50 else 1

    def line_9() -> int:
        answer["B"] = box[3]
        return 10

    lines = {
        1: lambda: double_jump(5, 1),
        2: lambda: double_jump(3, 2),
        3: line_3,
        4: line_4,
        5: line_5,
        6: line_6,
        7: line_7,
        8: line_8,
        9: line_9,
    }

    line = 1
    step = 0
    while line != 10:
        line_now = line
        line = lines[line_now]()
        step += 1
        if trace:
            print(f"step {step:>2} | LINE {line_now} -> LINE {line:<2} | boxes {box} | answers {answer}")

    return answer


if __name__ == "__main__":
    result = run(trace=True)
    print()
    print(f"ANSWER - BOX A: {result.get('A')}")
    print(f"ANSWER - BOX B: {result.get('B')}")
