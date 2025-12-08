from pathlib import Path
from itertools import product
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
    
def part1(vectors,N):
    prod = [(a,b) for a,b in product(vectors,repeat = 2) if abs(a) < abs(b)]
    circuits = {v:i for i,v in enumerate(vectors)}
    distances = [(abs(a-b),a,b) for a,b in prod]
    distances = sorted(distances,key = lambda x:x[0])
    for d,a,b in distances[:N]:
        continue

if __name__ == "__main__": 
    vectors = parse_input('test.txt')

    