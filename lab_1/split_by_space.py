import re


def extract(regex, test_cases):
    return map(lambda x: re.split(regex, x), test_cases)


def fmt_is_found_msg(m):
    return f"The {len(m)} elements(s) in the string is/are: {m}."


if __name__ == "__main__":
    tests = [
        "TheSpain",
        "The rain in Spain",
        "I've been to Spain",
    ]
    regex = re.compile(r"\s")
    results = extract(regex, tests)
    for test, res in zip(tests, results):
        print(f"In '{test}', {fmt_is_found_msg(res)}")
