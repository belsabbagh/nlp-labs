import re


def test_re(regex, test_cases):
    return map(lambda x: re.match(regex, x), test_cases)


def fmt_is_found_msg(m):
    return "Found it!" if m else "It's not there."


if __name__ == "__main__":
    tests = [
        "TheSpain",
        "The rain in Spain",
        "I've been to Spain",
    ]
    regex = re.compile(r"^The.*Spain$")
    results = test_re(regex, tests)
    for test, res in zip(tests, results):
        print(f"In '{test}', {fmt_is_found_msg(res)}")
