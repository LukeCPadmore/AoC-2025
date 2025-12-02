from pathlib import Path
def convert_to_instructions(line) -> tuple[str,int]:
    rotation = line[0] 
    amount = int(line[1:])
    return rotation, amount

def part1(filepath: Path) -> int:
    curr = 50
    hits_zero = 0
    with open(filepath) as f: 
        for line in f: 
            rotation, amount = convert_to_instructions(line)
            if rotation == 'L':
                curr -= amount
            else:
                curr += amount
            curr %= 100
            if curr == 0:
                hits_zero +=1
    return hits_zero

def part2(filepath: Path) -> int:
    curr = 50
    hits_zero = 0
    with open(filepath) as f: 
        for line in f:
            rotation, amount = convert_to_instructions(line)
            if rotation == 'L':
                dist0 = curr
            else: 
                dist0 = 100 - curr

            if dist0 == 0:
                dist0 = 100

            hits_zero += 1 + (amount - dist0) // 100

            if rotation == 'L':
                curr -= amount
            else: 
                curr += amount
            curr %= 100
    return hits_zero

if __name__ == "__main__":
    print(f'Solution to part 1: {part1("input.txt")}')
    print(f'Solution to part 2: {part2("input.txt")}')
        
            