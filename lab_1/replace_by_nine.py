import re


def extract(regex, repl, test_cases):
    return map(lambda x: re.sub(regex, repl, x, count=2), test_cases)


def fmt_is_found_msg(m):
    return f"The text becomes: {m}."


if __name__ == "__main__":
    tests = [
        "TheSpain",
        "The rain in Spain",
        "I've been to Spain",
    ]
    regex = re.compile(r"\s")
    results = extract(regex, "9", tests)
    for test, res in zip(tests, results):
        print(f"In '{test}', {fmt_is_found_msg(res)}")
