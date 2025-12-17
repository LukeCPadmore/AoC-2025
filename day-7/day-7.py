from pathlib import Path
from collections import deque, defaultdict
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def part1(filepath: Path) -> int:
    with open(filepath) as f:
        line = f.readline()
        # Read first line
        beams = {*find(line,"S")}
        num_splits = 0
        for line in f:
            splitters = find(line,'^')
            for splitter in splitters:
                if splitter in beams:
                    beams.remove(splitter)
                    beams.update([splitter - 1, splitter + 1])
                    num_splits +=1
    return num_splits

def part2(filepath: Path) -> int:
    with open(filepath) as f:
        line = f.readline()
        starting_state = (0,find(line,"S")[0])
        ways = defaultdict(int)
        frontiers = defaultdict(set)
        ways[starting_state] = 1
        frontiers[0].add(starting_state)
        for i,line in enumerate(f,0):
            splitters = find(line,'^')
            for level,pos in frontiers[i]:
                if pos in splitters:
                    left_new_state = (level + 1, pos - 1)
                    right_new_state = (level + 1, pos + 1)
                    # Check if new states are already seen, if not add to deque 
                    if left_new_state not in frontiers[i+2]:
                        frontiers[i+1].add(left_new_state)
                    if right_new_state not in frontiers[i+2]:
                        frontiers[i+1].add(right_new_state)
                    ways[left_new_state] += ways[(level, pos)]
                    ways[right_new_state] += ways[(level, pos)]
                else:
                    down_state = (level + 1, pos)
                    frontiers[level + 1].add(down_state)
                    ways[down_state] += ways[(level, pos)]
    bottom_level = max(frontiers.keys())
    return sum(ways[(level,pos)] for level,pos in frontiers[bottom_level])

def part1(filepath: Path) -> int:
    with open(filepath) as f:
        line = f.readline()
        # Read first line
        beams = {*find(line,"S")}
        num_splits = 0
        for line in f:
            splitters = find(line,'^')
            for splitter in splitters:
                if splitter in beams:
                    beams.remove(splitter)
                    beams.update([splitter - 1, splitter + 1])
                    num_splits +=1
    return num_splits
            

if __name__ == "__main__":
    #print(part1('input.txt'))
    print(part2('input.txt'))