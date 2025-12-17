from pathlib import Path
import itertools
from collections import Counter
import math
class Vector():
    def __init__(self,x:int,y:int,z:int) -> None:
        self.x, self.y, self.z = int(x),int(y),int(z)

    def __sub__(self,other:"Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __abs__(self) -> int:
        return self.x**2 + self.y**2 + self.z**2
    def __repr__(self) -> str:
        return f'({self.x},{self.y},{self.z})'
    
    def __eq__(self,other) -> bool:
            return isinstance(other, type(self)) and (self.x, self.y, self.z) == (other.x, other.y, other.z)
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
def parse_input(filepath:Path) -> None:
    vectors = []
    with open(filepath) as f:
        for line in f:
            vectors.append(Vector(*line.strip().split(",")))
    return vectors
    
def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent,x,y) -> bool:
    rx = find(parent, x)
    ry = find(parent, y)
    # Not connected so connect
    if rx != ry:
        parent[ry] = rx
        return True
    return False

    
def part1(vectors,N,k):
    pairs = list(itertools.combinations(vectors, 2))
    circuits = {v:v for v in vectors}
    distances = [(abs(a-b),a,b) for a,b in pairs]
    distances = sorted(distances,key = lambda x:x[0])
    for _,a,b in distances[:N+1]:
        union(circuits, a, b)
    roots = [find(circuits, v) for v in vectors]
    counts = Counter(roots)
    vals = sorted(counts.values(), reverse=True)
    return math.prod(vals[:k])

def part2(vectors):
    pairs = list(itertools.combinations(vectors, 2))
    circuits = {v:v for v in vectors}
    num_circuits = len(vectors)
    distances = [(abs(a-b),a,b) for a,b in pairs]
    distances = sorted(distances,key = lambda x:x[0])
    for _,a,b in distances:
        num_circuits -= union(circuits, a, b)
        if num_circuits == 1:
            return a.x * b.x
        
if __name__ == "__main__": 
    vectors = parse_input('input.txt')
    print(part1(vectors,1000,3))
    print(part2(vectors))