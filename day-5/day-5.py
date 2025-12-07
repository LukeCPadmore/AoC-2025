from pathlib import Path
from bisect import bisect_left, bisect_right

def parse_input(filepath:Path) -> (list[str],list[int]):
    ranges = [] 
    queries = []
    space_hit = False
    with open(filepath) as f:
        for line in f:
            if line.isspace():
                space_hit = True
                continue
            if not space_hit:
                ranges.append([int(n) for n in line.strip().split("-")])
            else:
                queries.append(int(line.strip()))
    return ranges,queries

def merge_ranges(ranges):
    ranges.sort()
    merged = [ranges[0]]

    for start, end in ranges:
        prev_start, prev_end = merged[-1]
        # intervals need to be merged as the overlap
        if start <= prev_end:
            merged[-1] = [prev_start, max(end,prev_end)]
        # else no overlap 
        else:
            merged.append([start,end])

    return merged

def filter_queries(query,starts,ends):
    return bisect_right(starts,query) > bisect_left(ends,query) and query < ends[-1] and query > starts[0]

def part1(ranges,queries) -> int: 
    starts,ends = zip(*merge_ranges(ranges))
    return len([query for query in queries if filter_queries(query,starts,ends)])

def part2(ranges) -> int:
    return sum([end - start + 1 for start,end in merge_ranges(ranges)])
if __name__ == "__main__":
    ranges, queries = parse_input('input.txt')
    print(part1(ranges,queries))
    print(part2(ranges))
