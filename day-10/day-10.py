from pathlib import Path
import re 
import numpy as np
import itertools
from collections import deque
from ortools.sat.python import cp_model
def parse_lights(line:str): 
    m = re.search(r"\[[.#]+\]",line)
    start, end = m.span()
    b = np.array([1 if c == '#' else 0 for c in line[start+1:end-1]])
    return b 

def parse_joltage(line:str):
    m = re.search(r"\{[0-9]+(,[0-9]+)*\}",line)
    start, end = m.span()
    return np.array(list(map(int, line[start + 1: end - 1].split(","))))

def parse_buttons(line:str,num_lights):
    matches = re.finditer(r"\([0-9]+(?:,[0-9]+)*\)", line)
    buttons = [list(map(int,m.group()[1:-1].split(','))) for m in matches]
    A = np.zeros((len(buttons),num_lights))
    for i in range(len(buttons)):
        for idx in buttons[i]:
            A[i,idx] = 1
    return A

def min_buttons_part1(A,b):
    xs = [np.array(x) for x in itertools.product([0,1],repeat = A.shape[0])]
    min_presses = float("inf")
    for x in xs:
        ok = np.all((A.T @ x) % 2 == b)
        if ok:
            min_presses = min(min_presses,sum(x))
    return min_presses
    

def part1(filename) -> None:
    num_buttons = 0
    with open(filename) as f:
        for line in f:
            b = parse_lights(line)
            A = parse_buttons(line,len(b))
            j = parse_joltage(line)
            num_buttons += min_buttons_part1(A,b)
    return num_buttons

def min_presses_joltage(A, target):
    start = np.zeros(target.shape)
    goal = tuple(target)
    q = deque([(start, 0)])
    seen = {tuple(start)}

    while q:
        state, d = q.popleft()
        if (state == goal).all():
            return d
        for v in A:
            nxt = state + v
            if all(nxt[i] <= goal[i] for i in range(len(target))) and tuple(nxt) not in seen:
                seen.add(tuple(nxt))
                q.append((nxt, d+1))

def solve_ilp_l1(A, b):
    A = np.asarray(A, dtype=int)
    b = np.asarray(b, dtype=int).reshape(-1)

    k, m = A.shape
    assert b.shape[0] == k, (A.shape, b.shape)

    model = cp_model.CpModel()

    x = []
    for j in range(m):
        rows = np.where(A[:, j] != 0)[0]
        ub = int(b[rows].min()) if len(rows) else 0
        x.append(model.NewIntVar(0, ub, f"x{j}"))

    for i in range(k):
        model.Add(sum(int(A[i, j]) * x[j] for j in range(m)) == int(b[i]))

    model.Minimize(sum(x))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return int(solver.ObjectiveValue()), [solver.Value(v) for v in x]
    return None, None

def part2(filename:Path) -> None:
    total = 0
    with open(filename) as f:
        for line in f:
            j = parse_joltage(line)
            A = parse_buttons(line,len(j))
            presses,_ = solve_ilp_l1(A.T,j)
            total += presses
    return total

if __name__ == "__main__":
    # print(part1("input.txt"))
    print(part2("input.txt"))

