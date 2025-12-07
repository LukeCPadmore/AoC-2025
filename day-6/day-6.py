from pathlib import Path
import math
def parse_file_part1(filepath) -> list[str]:
    with open(filepath) as f:
        blocks = [line.strip().split(' ') for line in f]
        blocks = [[s for s in block if s] for block in blocks]
        return blocks

def parse_file_part2(filepath) -> list[str]:
    with open(filepath) as f:
        blocks = [line.strip('\n') for line in f]
        blocks = [[s for s in block if s] for block in blocks]
        return blocks

def part1(blocks) -> int:
    blocks[:-1] = [[int(s) for s in block if s] for block in blocks[:-1]]
    trans = [*zip(*blocks)]
    calc = lambda x: sum(x[:-1]) if x[-1] == '+' else math.prod(x[:-1])
    return sum([calc(block) for block in trans])

def part2(blocks) -> int:
    block_idx = [i for i in range(len(blocks[-1])) if blocks[-1][i] != ' ']
    block_idx.append(len(blocks[0]))
    ops = [blocks[-1][i] for i in block_idx[:-1]]

    temp = [[block[i:j] for block in blocks[:-1]] for i,j in zip(block_idx[:-1],block_idx[1:])]
    cols = [["".join(list(col)) for col in zip(*block)] for block in temp]

    nums = [[*[int(s) for s in col if not s.isspace()],op] for col,op in zip(cols,ops)]
    calc = lambda x: sum(x[:-1]) if x[-1] == '+' else math.prod(x[:-1])
    return sum([calc(block) for block in nums])
if __name__ == "__main__": 
    # blocks = parse_file_part1('input.txt')
    # print(part1(blocks))
    blocks = parse_file_part2('input.txt')
    print(part2(blocks))