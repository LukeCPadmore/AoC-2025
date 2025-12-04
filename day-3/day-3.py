from pathlib import Path
from typing import List
from collections.abc import Generator

def argmax(arr) -> int:
    return max(range(len(arr)), key=lambda x: arr[x])

def parse_lines(filepath: Path) -> Generator[List[int],None, None]:
    with open(filepath) as f:
        return [[int(ch) for ch in line.strip()] for line in f]

def part1(banks) -> int:
    def largest_joltage(bank) -> int: 
        l = max(range(len(bank) - 1), key=lambda x: bank[x])
        r = max(range(l,len(bank)), key=lambda x: bank[x])
        return bank[l] * 10 + bank[r]
    return sum([largest_joltage(bank) for bank in banks])

def part2(banks) -> int:
    def largest_joltage(bank) -> int: 
        chosen_indices = []
        p = 0 
        for i in range(0,12):
            limit = len(bank) - (12 - i)
            best_index = argmax(bank[p:limit + 1])
            chosen_indices.append(str(bank[p + best_index]))
            p += best_index + 1
        return int("".join(chosen_indices))
    return sum(largest_joltage(bank) for bank in banks)

if __name__ == "__main__":
    banks = parse_lines('input.txt')
    print(part1(banks))
    print(part2(banks))