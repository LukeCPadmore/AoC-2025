from pathlib import Path
from itertools import combinations
def parse_file(filepath:Path):
    with open(filepath) as f:
        return [[*map(int,line.strip().split(","))] for line in f]

def calc_area(x1,y1,x2,y2):
    return (max(x1,x2) - min(x1,x2) + 1) * (max(y1,y2) - min(y1,y2) + 1)

def part1(tiles):
    return max(
        calc_area(x1, y1, x2, y2)
        for (x1, y1), (x2, y2) in combinations(tiles, 2)
    )

if __name__ == "__main__":
    tiles = parse_file('input.txt') 
    print(part1(tiles))
