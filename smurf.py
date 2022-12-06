import math
import sys
from functools import reduce

class Segment:
    def __init__(self, id, coorX, coorY, connections):
        self.id = id
        self.coorX = coorX
        self.coorY = coorY
        self.connections = connections

# class Path:
#     def __init__(self, start, stop, distance):
#         self.segments = segments


filename = sys.argv[1]
segments = {}

with open(filename, 'r') as file:
    line = file.readline()
    cnt = 0
    while line:
        print(line)
        delim = line.strip().split(' ')
        id = int(delim[0])
        coorX, coorY = float(delim[1]), float(delim[2])
        connections = list(map(int, delim[3:]))
        segments[id] = Segment(id, coorX, coorY, connections)
        line = file.readline()

print("File has been successfully read")

# ## ----------------
# ## Show summary

# ## ----------------
print(len(segments))

def getDistance(seg1: Segment, seg2: Segment) -> float:
    return math.dist([seg1.coorX, seg1.coorY], [seg2.coorX, seg2.coorY])

def getTotalDistance(input: list[int]) -> float:
    global segments
    distance = 0
    for i in range(len(input) - 1):
        segID = input[i]
        nextSegID = input[i+1]
        distance += getDistance(segments[segID], segments[nextSegID])
        
    return distance

def findRoute(seg: Segment, previousStack: list[int]) -> None:
    global segments, paths
    stack = [node for node in previousStack]
    stack.append(seg.id)

    for conn in seg.connections:
        if len(stack) > 1 and conn == stack[0]:
            stack2 = [node for node in stack]
            stack2.append(conn)
            paths[str(stack2)] = round(getTotalDistance(stack2), 2)
        elif (conn not in stack):
            findRoute(segments[conn], stack)

paths = {}

for seg in segments.values():
    findRoute(seg, [])

for key, value in paths.items():
    print(key, ':', value)

