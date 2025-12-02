from pathlib import Path
from typing import Any
def parse_input(filepath: Path) -> Any:
    with open(filepath) as f:
        ranges = f.readline().split(',')
    return [*map(lambda x: x.split('-'),ranges)]

def check_invalid_id(num_str:str):
    mid = len(num_str) // 2
    if len(num_str) % 2 == 0:
        mid = len(num_str) // 2 
        first = int(num_str[:mid])
        second = int(num_str[mid:])
        return first - second == 0
    return False

def get_ids(ranges):
    return [str(i) for start, end in ranges
           for i in range(int(start), int(end) + 1)]
def part1(ranges) -> int:
    return sum([int(i) for i in filter(check_invalid_id,get_ids(ranges))])

def part2() -> int: 
    pass

if __name__ == "__main__":
    ranges = parse_input('input.txt')
    print(part1(ranges))
