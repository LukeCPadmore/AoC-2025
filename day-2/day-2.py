from pathlib import Path
from typing import Any
import math
def parse_input(filepath: Path) -> Any:
    with open(filepath) as f:
        ranges = f.readline().split(',')
    return [*map(lambda x: x.split('-'),ranges)]


def get_ids(ranges):
    return [str(i) for start, end in ranges
           for i in range(int(start), int(end) + 1)]

def part1(ranges) -> int:
    def check_invalid_id(num_str:str):
        mid = len(num_str) // 2
        if len(num_str) % 2 == 0:
            mid = len(num_str) // 2 
            first = int(num_str[:mid])
            second = int(num_str[mid:])
            return first - second == 0
        return False
    return sum([int(i) for i in filter(check_invalid_id,get_ids(ranges))])

def get_factors(n:int) -> list[int]:
    factors = {1}
    if n == 2:
        return factors
    for i in range(2,math.ceil(math.sqrt(n)) + 1):
        if n % i == 0:
            if n // i == i:
                factors.add(i)
            else: 
                factors.update([i , n // i])
    return factors

def check_valid_split(num_str:str, n:int) -> bool:
    splits = [num_str[i*n:(i+1)*n] for i in range(0,len(num_str) // n)]
    return all(s == splits[0] for s in splits)

def check_any_splt_valid(num_str):
    return any([check_valid_split(num_str,factor) for factor in get_factors(len(num_str))])

def part2(ranges) -> int: 
    def get_factors(n:int) -> list[int]:
        factors = {1}
        if n == 2:
            return factors
        for i in range(2,math.ceil(math.sqrt(n)) + 1):
            if n % i == 0:
                if n // i == i:
                    factors.add(i)
                else: 
                    factors.update([i , n // i])
        return factors

    def check_valid_split(num_str:str, n:int) -> bool:
        splits = [num_str[i*n:(i+1)*n] for i in range(0,len(num_str) // n)]
        return all(s == splits[0] for s in splits)

    def check_any_splt_valid(num_str):
        if len(num_str) < 2:
            return False
        return any([check_valid_split(num_str,factor) for factor in get_factors(len(num_str))])
    
    return sum([int(i) for i in filter(check_any_splt_valid,get_ids(ranges))]) 

if __name__ == "__main__":
    # More efficient way according to Chatgpt is to generate all invalid ids and check if they are in the ranges
    ranges = parse_input('input.txt')
    print(part1(ranges))
    print(part2(ranges))
    
