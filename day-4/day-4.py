from pathlib import Path
from typing import List
from itertools import product
def parse_grid(filename:Path) -> List[List[str]]: 
    with open(filename) as f: 
        return [list(line.strip()) for line in f] 


def part1(grid) -> int: 
    M = len(grid)
    N = len(grid[0])
    accessible = [] 
    dirs = set(product([-1,0,1],[-1,0,1]))
    dirs.remove((0,0))
    for i in range(M):
        for j in range(N):
            if grid[i][j] != '@':
                continue
            rolls = 0
            for dir in dirs:
              if rolls >= 4:
                  break
              ver, hor = dir
              x = i + ver
              y = j + hor
              if x < 0 or x >= M or y < 0 or y>= N:
                  continue
              if grid[x][y] == '@':
                  rolls += 1
            if rolls < 4:
                accessible.append((i,j))
    return accessible

def part2(grid) -> int:
    total = 0
    while True:
        accessible = part1(grid) 
        if not accessible:
            return total
        total += len(accessible)
        for x,y in accessible:
            grid[x][y] = '.'
    

if __name__ == "__main__": 
    grid = parse_grid('input.txt')
    print(len(part1(grid)))
    print(part2(grid))
