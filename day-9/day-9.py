from pathlib import Path
from itertools import combinations
from collections import deque

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

def build_lists(tiles):
    x_list, y_list = set(), set()
    for x,y in tiles:
        x_list.update([x-1,x,x+1])
        y_list.update([y-1,y,y+1])
    x_list = sorted(x_list)
    y_list = sorted(y_list)
    x_index = {x:i for i,x in enumerate(x_list)}
    y_index = {y:i for i,y in enumerate(y_list)}
    return x_index, x_list, y_index, y_list

def build_edges(tiles):
    edges = [[tiles[0],tiles[-1]]]
    edges.extend([[t1,t2] for t1,t2 in zip(tiles[:-1],tiles[1:])])
    return edges

def mark_boundary(edges, x_index, y_index):
    boundary = set()
    for p1, p2 in edges:
        # Horizontal edge: y constant
        if p1[1] == p2[1]:
            a = min(p1[0], p2[0])
            b = max(p1[0], p2[0])
            a_index = x_index[a]
            b_index = x_index[b]
            y_idx = y_index[p1[1]]
            # mark columns between a and b
            for i in range(a_index, b_index):
                boundary.add((i, y_idx))
        else:
            # Vertical edge: x constant
            a = min(p1[1], p2[1])
            b = max(p1[1], p2[1])
            a_index = y_index[a]
            b_index = y_index[b]
            x_idx = x_index[p1[0]]
            for j in range(a_index, b_index):
                boundary.add((x_idx, j))
    return boundary



def flood_fill_outside(boundary: set[tuple[int, int]], W: int, H: int):
    def in_bounds(x, y):
        return 0 <= x < W and 0 <= y < H

    outside = set()
    q = deque()

    # seed BFS with all non-blocked border cells
    for x in range(W):
        for y in (0, H - 1):
            if (x, y) not in boundary and (x, y) not in outside:
                outside.add((x, y))
                q.append((x, y))

    for y in range(H):
        for x in (0, W - 1):
            if (x, y) not in boundary and (x, y) not in outside:
                outside.add((x, y))
                q.append((x, y))

    # BFS 4-neighbour
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and (nx, ny) not in boundary and (nx, ny) not in outside:
                outside.add((nx, ny))
                q.append((nx, ny))

    return outside


def cell_area(outside, x_list, y_list):
    H = len(y_list) - 1
    W = len(x_list) - 1
    A = [[0] * W for _ in range(H)]

    for r in range(H):
        for c in range(W):
            # (c, r) are cell coords (x, y)
            if (c, r) not in outside:
                width  = x_list[c+1] - x_list[c]
                height = y_list[r+1] - y_list[r]
                A[r][c] = width * height

    # build prefix sum
    PS = [[0] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            PS[r][c] = A[r][c]
            if r > 0:
                PS[r][c] += PS[r-1][c]
            if c > 0:
                PS[r][c] += PS[r][c-1]
            if r > 0 and c > 0:
                PS[r][c] -= PS[r-1][c-1]
    return PS


def rect_sum(PS, r1, c1, r2, c2):
    res = PS[r2-1][c2-1]
    if r1 > 0:
        res -= PS[r1-1][c2-1]
    if c1 > 0:
        res -= PS[r2-1][c1-1]
    if r1 > 0 and c1 > 0:
        res += PS[r1-1][c1-1]
    return res


def part2(tiles):
    x_index, x_list, y_index, y_list = build_lists(tiles)
    edges = build_edges(tiles)
    boundary = mark_boundary(edges, x_index, y_index)

    W = len(x_list) - 1
    H = len(y_list) - 1

    outside = flood_fill_outside(boundary, W, H)
    PS = cell_area(outside, x_list, y_list)

    max_area = 0

    for t1, t2 in combinations(tiles, 2):
        x1, y1 = t1
        x2, y2 = t2

        # skip degenerate rectangles (line segments)
        if x1 == x2 or y1 == y2:
            continue

        x_lo, x_hi = min(x1, x2), max(x1, x2)
        y_lo, y_hi = min(y1, y2), max(y1, y2)

        # indices for *tile-inclusive* rectangle: [x_lo, x_hi] × [y_lo, y_hi]
        # → in compressed coords, we use [x_lo, x_hi+1), [y_lo, y_hi+1)
        c1 = x_index[x_lo]
        c2 = x_index[x_hi + 1]
        r1 = y_index[y_lo]
        r2 = y_index[y_hi + 1]

        true_area = (x_list[c2] - x_list[c1]) * (y_list[r2] - y_list[r1])

        if true_area == rect_sum(PS, r1, c1, r2, c2):
            max_area = max(max_area, true_area)

    return max_area


        
        
def print_grid(boundary, inside=None, outside=None):
    # Determine grid size from boundary + any filled sets
    all_points = set(boundary)
    if inside:
        all_points |= inside
    if outside:
        all_points |= outside

    max_x = max(x for x, y in all_points)
    max_y = max(y for x, y in all_points)

    for y in range(max_y, -1, -1):   # top to bottom
        row = []
        for x in range(max_x + 1):
            if (x, y) in boundary:
                row.append("#")      # boundary
            elif inside and (x, y) in inside:
                row.append("I")      # inside
            elif outside and (x, y) in outside:
                row.append("O")      # outside
            else:
                row.append(".")      # unknown / free
        print("".join(row))




if __name__ == "__main__":
    tiles = parse_file('input.txt')
    part1(tiles)
    part2(tiles)
