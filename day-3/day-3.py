from pathlib import Path
from typing import List
from collections.abc import Generator


def parse_lines(filepath: Path) -> Generator[List[int],None, None]:
    with open(filepath) as f:
        return [[int(ch) for ch in line.strip()] for line in f]

def part1(banks) -> int:
    def largest_joltage(bank) -> int: 
        l = max(range(len(bank) - 1), key=lambda x: bank[x])
        r = max(range(l + 1, len(bank)), key=lambda x: bank[x])
        return bank[l] * 10 + bank[r]
    return sum([largest_joltage(bank) for bank in banks])

def part2(banks) -> int:
    def largest_joltage(bank) -> int: 
        d = {i:bank[i] for i in range(len(bank))}
        indices_to_remove = sorted(range(len(bank)), key = lambda x:(bank[x],x))[:-12]
        return int("".join([str(bank[i]) for i in range(len(bank)) if i not in indices_to_remove]))
    print([largest_joltage(bank) for bank in banks])
    return sum(largest_joltage(bank) for bank in banks)

if __name__ == "__main__":
    banks = parse_lines('test.txt')
    print(part1(banks))
    print(part2(banks))