import re
from collections import Counter

def extract(regex, test_cases):
    return map(lambda x: re.findall(regex, x), test_cases)


def fmt_is_found_msg(m):
    counts = Counter(m)
    return "There's nothing there" if not m else f"Found these characters this many times: {dict(counts)}"


if __name__ == "__main__":
    tests = [
        "T3heS4pain8",
        "8 times before 11:45PM",
        "I've been to Spain",
    ]
    regex = re.compile(r"\d")
    results = extract(regex, tests)
    for test, res in zip(tests, results):
        print(f"In '{test}', {fmt_is_found_msg(res)}")
