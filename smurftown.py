import logging
import math
import sys
from functools import reduce

class Segment:
    def __init__(self, id, coorX, coorY, connections):
        self.id = id
        self.coorX = coorX
        self.coorY = coorY
        self.connections = connections

class Route:
    def __init__(self, path, distance):
        self.path = path
        self.distance = distance

filename = sys.argv[1]
segments = {}

with open(filename, 'r') as file:
    line = file.readline()
    while line:
        delim = line.strip().split(' ')
        id = int(delim[0])
        coorX, coorY = float(delim[1]), float(delim[2])
        connections = list(map(int, delim[3:]))
        segments[id] = Segment(id, coorX, coorY, connections)
        line = file.readline()

print("File has been successfully read")

def getDistanceBetweenTwoNodes(seg1: Segment, seg2: Segment) -> float:
    return math.dist([seg1.coorX, seg1.coorY], [seg2.coorX, seg2.coorY])

def getTotalDistanceFromSegmentList(input: list[int]) -> float:
    global segments
    distance = 0
    for i in range(len(input) - 1):
        segID = input[i]
        nextSegID = input[i+1]
        distance += getDistanceBetweenTwoNodes(segments[segID], segments[nextSegID])
        
    return distance

def getRouteLengthOfStartSegment(segmentID: int) -> float:
    global loopingRoutes
    if segmentID in loopingRoutes.keys():
        return loopingRoutes[segmentID].distance
    else:
        return 0 

def findLoopingRoutes(seg: Segment, previousStack: list[int]) -> None:
    global segments, loopingRoutes
    stack = [node for node in previousStack]
    stack.append(seg.id)

    for conn in seg.connections:
        if len(stack) > 1 and conn == stack[0]:
            loopingStack = [node for node in stack]
            loopingStack.append(conn)
            routeLength = round(getTotalDistanceFromSegmentList(loopingStack), 2)
            
            ## If a route with the same starting point already exists, replace it with the one that has the longest distance
            if routeLength > getRouteLengthOfStartSegment(stack[0]):
                route = Route(str(loopingStack), round(getTotalDistanceFromSegmentList(loopingStack), 2))
                loopingRoutes[stack[0]] = route

        elif (conn not in stack):
            findLoopingRoutes(segments[conn], stack)

loopingRoutes = {}

print("Checking possible routes....")
for seg in segments.values():
    findLoopingRoutes(seg, [])

print("Found the longest route")
maxDistance = max([route.distance for route in loopingRoutes.values()])
## Sort and filter the routes in order to remove the same cyclic patterns that start from a higher ID
longestPathWithLowestID = sorted([route.path for route in loopingRoutes.values() if route.distance == maxDistance])[0]
print(longestPathWithLowestID)
