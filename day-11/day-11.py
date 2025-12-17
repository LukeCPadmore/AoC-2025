from pathlib import Path
from collections import defaultdict, deque
def parse_input(filename:Path) -> dict[str,list[str]]:
    adj_list = defaultdict(list)
    with open(filename) as f:
        for line in f:
            k,v = line.strip().split(':')
            adj_list[k] = v.split()
        return adj_list
    
def compute_indegree(adj_list,start):
    indegree = defaultdict(int)
    for u in adj_list.keys():
        indegree[u] += 0
        for v in adj_list[u]:
            indegree[v] +=1
    indegree[start] = 0
    return indegree

def part1(adj_list,start,end) -> int: 
    indegree = compute_indegree(adj_list,start=start)
    frontier = deque([n for n,d in indegree.items() if d == 0])
    ways = defaultdict(int,{start:1})
    while frontier:
        curr = frontier.popleft()
        next_nodes = adj_list[curr]
        for node in next_nodes:
            ways[node] += ways[curr]
            indegree[node] -= 1
            if indegree[node] == 0:
                frontier.append(node)
    return ways[end]

def reachable(adj_list,start,target):
    frontier = deque([start])
    seen = set([start])
    while frontier:
        curr = frontier.popleft()
        next_nodes = adj_list[curr]
        for node in next_nodes:
            if node == target:
                return True
            if node not in seen:
                frontier.append(node)
                seen.add(node)
    return False

def part2(adj_list,start,end):
    if reachable(adj_list,'fft','dac'):
        first, second = 'fft','dac'
    else:
        first, second = 'dac','fft'
    return part1(adj_list,start,first) * part1(adj_list,first,second) * part1(adj_list,second,end)

if __name__ == "__main__":
    adj_list = parse_input('input.txt')
    print(part1(adj_list,start= 'you',end = 'out'))
    print(part2(adj_list,'svr','out'))
        