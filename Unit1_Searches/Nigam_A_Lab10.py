# Name: Arul Nigam Date: 10/09/2019

import heapq, random, pickle, math, time
from math import pi, acos, sin, cos
from tkinter import *
from collections import deque


class PriorityQueue():
    def __init__(self):
        self.current = None
        self.queue = []
        current = 0  # to make this object iterable

    # To make this object iterable: have __iter__ function and assign next function for __next__
    def next(self):
        if self.current >= len(self.queue):
            raise StopIteration
        out = self.queue[self.current]
        self.current += 1
        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 0

    ''' complete the following functions '''

    def remove(self, index):
        rem = self.queue[index]
        del self.queue[index]
        return rem

    def pop(self):
        # swap first and last. Remove last. Heap down from first.
        self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
        rem = self.queue[-1]
        del self.queue[-1]
        first = 0
        last = len(self.queue) - 1
        while last >= (first * 2 + 1):
            lchild = min((first * 2 + 1), last)
            rchild = min((first * 2 + 2), last)
            child = lchild
            if self.queue[lchild] > self.queue[rchild]:
                child = rchild
            if self.queue[first] > self.queue[child]:
                self.queue[first], self.queue[child] = self.queue[child], self.queue[first]
                first = child
            else:
                first = last
        # return the removed value
        return rem

    def push(self, value):
        # append at last. Heap up.
        self.queue.append(value)
        last = len(self.queue) - 1
        while last > 0:
            next_last = int((last - 1) / 2)
            if self.queue[last] < self.queue[next_last]:
                self.queue[last], self.queue[next_last] = self.queue[next_last], self.queue[last]
            last = next_last
        pass

    def peek(self):
        return self.queue[0]

def calc_edge_cost(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R
    #

# NodeLocations, NodeToCity, CityToNode, Neighbors, EdgeCost
# Node: (lat, long) or (y, x), node: city, city: node, node: neighbors, (n1, n2): cost
def make_graph(nodes="rrNodes.txt", node_city="rrNodeCity.txt", edges="rrEdges.txt"):
    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
    map = {}  # have screen coordinate for each node location # pixel coordinates
    nodeLoc = populate_nodeLoc()
    nodeToCity, cityToNode = populate_nodeToCity_and_cityToNode()
    neighbors, edgeCost = populate_neighbors_and_edgeCost(nodeLoc)
    map = populate_map(nodeLoc)
    return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]

def populate_nodeLoc(fileName="rrNodes.txt"):
    nodeLoc = {}
    file = open(fileName, "r")
    for nodeInfo in file.readlines():
        nodeInfo = nodeInfo.rstrip('\n')
        nodeInfoList = nodeInfo.split(" ")
        name = nodeInfoList[0]
        latitude = nodeInfoList[1]
        longitude = nodeInfoList[2]
        nodeLoc[name] = [latitude, longitude]
    file.close()
    return nodeLoc

def populate_nodeToCity_and_cityToNode(fileName="rrNodeCity.txt"):
    nodeToCity, cityToNode = {}, {}
    file = open(fileName, "r")
    for nodeInfo in file.readlines():
        nodeInfo = nodeInfo.rstrip('\n')
        nodeInfoList = nodeInfo.split(" ")
        node = nodeInfoList[0]
        city = nodeInfoList[1]
        if len(nodeInfoList) > 2:
            for i in range(2, len(nodeInfoList)):
                city += " "
                city += nodeInfoList[i]
        nodeToCity[node] = city
        cityToNode[city] = node
    file.close()
    return nodeToCity, cityToNode

def populate_neighbors_and_edgeCost(nodeLoc, fileName="rrEdges.txt"):  # a:b and b:a
    neighbors, edgeCost = {}, {}
    file = open(fileName, "r")
    for nodeInfo in file.readlines():
        nodeInfo = nodeInfo.rstrip('\n')
        nodeInfoList = nodeInfo.split(" ")
        node1 = nodeInfoList[0]
        node2 = nodeInfoList[1]
        if node1 not in neighbors:
            neighbors[node1] = [node2]
        else:
            neighbors[node1].append(node2)
        if node2 not in neighbors:
            neighbors[node2] = [node1]
        else:
            neighbors[node2].append(node1)
        edgeCost[node1, node2] = calc_edge_cost(nodeLoc[node1][0], nodeLoc[node1][1], nodeLoc[node2][0], nodeLoc[node2][1])
        edgeCost[node2, node1] = edgeCost[node1, node2]
    file.close()
    return neighbors, edgeCost

def populate_map(nodeLoc):
    map = {}
    for node in nodeLoc:  # checks each
        lat = float(nodeLoc[node][0])  # gets latitude
        long = float(nodeLoc[node][1])  # gets long
        modlat = (lat - 10) / 60  # scales to 0-1
        modlong = (long + 130) / 70  # scales to 0-1
        map[node] = [modlat * 800, modlong * 1200]  # scales to fit 800 1200
    return map

# Return the direct distance from node1 to node2
# Use calc_edge_cost function.
def dist_heuristic(n1, n2, graph):
    return calc_edge_cost(graph[0][n1][0], graph[0][n1][1], graph[0][n2][0], graph[0][n2][1])

# Create a city path. 
# Visit each node in the path. If the node has the city name, add the city name to the path.
# Example: ['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
def display_path(path, graph):
    toDisplay = []
    for i in path:
        if i in graph[1]:
            toDisplay.append(graph[1][i])
    print(toDisplay)
    pass

# Using the explored, make a path by climbing up to "s"
# This method may be used in your BFS and Bi-BFS algorithms.
def generate_path(state, explored, graph, start):
    path, cost = [state], 0
    while explored[state] != start:  # assume the parent of root is "s"
        path.append(explored[state])
        cost += graph[4][state, explored[state]]
        state = explored[state]
    return path[::-1], cost + 1

def drawLine(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    canvas.create_line(x1, 800 - y1, x2, 800 - y2, fill=col)

# Draw the final shortest path.
# Use drawLine function.
def draw_final_path(ROOT, canvas, path, graph, col='red'):
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    size = len(path)
    for i in range(1, size):
        drawLine(canvas, graph[5][path[i - 1]][0], graph[5][path[i - 1]][1], graph[5][path[i]][0], graph[5][path[i]][1],
                 col)
    ROOT.update()
    pass

def draw_all_edges(ROOT, canvas, graph):
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    for n1, n2 in graph[4]:  # graph[4] keys are edge set
        drawLine(canvas, *graph[5][n1], *graph[5][n2], 'white')  # graph[5] is map dict
    ROOT.update()

def bfs(start, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    counter = 0
    frontier, explored = deque(), {start: "s"}
    frontier.append(start)
    while frontier:
        s = frontier.popleft()
        if s == goal:
            path, cost = generate_path(s, explored, graph, "s")
            draw_final_path(ROOT, canvas, path, graph)
            print("The number of explored nodes of BFS:", len(explored))
            print("The whole path:", path)
            print("The length of the whole path:", len(path))
            return path, cost
        for a in graph[3][s]:  # graph[3] is neighbors
            if a not in explored:
                explored[a] = s
                frontier.append(a)
                drawLine(canvas, *graph[5][s], *graph[5][a], col)
        counter += 1
        if counter % 100 == 0: ROOT.update()
    return None

def bi_bfs(start, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("Bi-directional BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    counter = 0
    frontierS, exploredS = deque(), {start: "s"}  # normal
    frontierS.append(start)
    frontierF, exploredF = deque(), {goal: "f"}  # backward
    frontierF.append(goal)
    while frontierS or frontierF:
        if frontierS:
            s = frontierS.popleft()
            if s == goal or s in frontierF:
                pathS, costS = generate_path(s, exploredS, graph, "s")
                pathF, costF = None, None
                if s in frontierF:
                    pathF, costF = generate_path(s, exploredF, graph, "f")
                    pathF.reverse()
                    path = pathS + pathF[1:]
                    cost = costS + costF
                else:
                    path = pathS
                    cost = costS
                draw_final_path(ROOT, canvas, path, graph)
                print("The number of explored nodes of Bi-directional BFS:", len(exploredS))
                print("The whole path:", path)
                print("The length of the whole path:", len(path))
                return path, cost
            for a in graph[3][s]:  # graph[3] is neighbors
                if a not in exploredS:
                    exploredS[a] = s
                    frontierS.append(a)
                    drawLine(canvas, *graph[5][s], *graph[5][a], col)
        if frontierF:
            f = frontierF.popleft()
            if f == start or f in frontierS:
                pathF, costF = generate_path(f, exploredF, graph, "f")
                pathF.reverse()
                pathS, costS = None, None
                if f in frontierS:
                    pathS, costS = generate_path(f, exploredS, graph, "s")
                    pathF[1:].reverse()
                    path = pathS + pathF[1:]
                    cost = costS + costF
                else:
                    path = pathF
                    cost = costF
                draw_final_path(ROOT, canvas, path, graph)
                print("The number of explored nodes of Bi-BFS:", len(exploredF))
                print("The whole path:", path)
                print("The length of the whole path:", len(path))
                return path, cost
            for a in graph[3][f]:  # graph[3] is neighbors
                if a not in exploredF:
                    exploredF[a] = f
                    frontierF.append(a)
                    drawLine(canvas, *graph[5][f], *graph[5][a], col)
        counter += 1
        if counter % 100 == 0: ROOT.update()
    return None

def a_star(start, goal, graph, col, heuristic=dist_heuristic):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("A*")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    counter = 0
    if start == goal:
        return [start, goal], graph[4][start, goal]
    frontier, explored = PriorityQueue(), {start: "s"}
    frontier.push((heuristic(start, goal, graph), start, [start]))
    old_explored = []
    while frontier:
        popped = frontier.pop()
        current_path = popped[2]  # path
        current_node = popped[1]
        cost = popped[0] - heuristic(current_node, goal, graph)
        if current_node == goal:  # current value
            path = current_path
            draw_final_path(ROOT, canvas, path, graph)
            print("The number of explored nodes of A*:", len(explored))
            print("The whole path:", path)
            print("The length of the whole path:", len(path))
            return path, cost
        if current_node not in old_explored:
            old_explored.append(current_node)
            for neighbor in graph[3][current_node]:  # graph[3] is neighbors
                if neighbor not in old_explored:
                    explored[neighbor] = current_node
                    new_cost = cost + graph[4][current_node, neighbor] + heuristic(neighbor, goal, graph)
                    frontier.push((new_cost, neighbor, current_path + [neighbor]))
                    drawLine(canvas, *graph[5][current_node], *graph[5][neighbor], col)
        counter += 1
        if counter % 100 == 0: ROOT.update()
    return None

def bi_a_star(start, goal, graph, col, heuristic=dist_heuristic):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("Bi-A*")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    counter = 0
    if start == goal:
        return [start, goal], graph[4][start, goal]
    frontierF, frontierB, exploredF, exploredB = PriorityQueue(), PriorityQueue(), {start: "s"}, {goal: "f"}
    frontierF.push((heuristic(start, goal, graph), start, [start]))
    frontierB.push((heuristic(goal, start, graph), goal, [goal]))
    old_exploredF = []
    old_exploredB = []
    while frontierF or frontierB:
        poppedF = frontierF.pop()
        poppedB = frontierB.pop()
        current_pathF = poppedF[2]  # path
        current_pathB = poppedB[2]  # path
        current_nodeF = poppedF[1]
        current_nodeB = poppedB[1]
        costF = poppedF[0] - heuristic(current_nodeF, goal, graph)
        costB = poppedB[0] - heuristic(current_nodeB, start, graph)
        if current_nodeF == goal:  # current value
            pathF = current_pathF
            draw_final_path(ROOT, canvas, pathF, graph)
            print("The number of explored nodes of Bi-A*:", len(exploredF))
            print("The whole path:", pathF)
            print("The length of the whole path:", len(pathF))
            return pathF, costF
        if current_nodeB == start:  # current value
            pathB = current_pathB
            draw_final_path(ROOT, canvas, pathB, graph)
            print("The number of explored nodes of Bi-A*:", len(exploredB))
            print("The whole path:", pathB)
            print("The length of the whole path:", len(pathB))
            return pathB[::-1], costB
        if (current_nodeF not in old_exploredF):
            old_exploredF.append(current_nodeF)
            for neighbor in graph[3][current_nodeF]:  # graph[3] is neighbors
                if neighbor not in old_exploredF:
                    exploredF[neighbor] = current_nodeF
                    new_cost = costF + graph[4][current_nodeF, neighbor] + heuristic(neighbor, goal, graph)
                    frontierF.push((new_cost, neighbor, current_pathF + [neighbor]))
                    drawLine(canvas, *graph[5][current_nodeF], *graph[5][neighbor], col) 
        if (current_nodeB not in old_exploredB):
            old_exploredB.append(current_nodeB)
            for neighbor in graph[3][current_nodeB]:  # graph[3] is neighbors
                if neighbor not in old_exploredB:
                    exploredB[neighbor] = current_nodeB
                    new_cost = costB + graph[4][current_nodeB, neighbor] + heuristic(neighbor, start, graph)
                    frontierB.push((new_cost, neighbor, current_pathB + [neighbor]))
                    drawLine(canvas, *graph[5][current_nodeB], *graph[5][neighbor], col)
        counter += 1
        if counter % 100 == 0: ROOT.update()
    return None

def tri_directional(city1, city2, city3, graph, col, heuristic=dist_heuristic):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("Tri-Directional")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    path12, cost12, explored_nodes12 = tri_directional_helper(city1, city2, graph, col, ROOT, canvas, heuristic)
    path23, cost23, explored_nodes23 = tri_directional_helper(city2, city3, graph, col, ROOT, canvas, heuristic)
    path31, cost31, explored_nodes31 = tri_directional_helper(city3, city1, graph, col, ROOT, canvas, heuristic)
    if (cost12 + cost23) < (cost23 + cost31) or (cost12 + cost23) < (cost12 + cost31):
      draw_final_path(ROOT, canvas, path12 + path23, graph)
      print("The number of explored nodes of Tri-directional Search:", explored_nodes12 + explored_nodes23)
      print("The whole path:", (path12 + path23[1:]))
      print("The length of the whole path:", len((path12 + path23[1:])))
      return (path12 + path23[1:]), (cost12 + cost23)
    elif (cost23 + cost31) < (cost12 + cost23) or (cost23 + cost31) < (cost12 + cost31):
      draw_final_path(ROOT, canvas, path23 + path31, graph)
      print("The number of explored nodes of Tri-directional Search:", explored_nodes23 + explored_nodes31)
      print("The whole path:", (path23 + path31[1:]))
      print("The length of the whole path:", len((path23 + path31[1:])))
      return (path23 + path31[1:]), (cost23 + cost31)
    elif (cost12 + cost31) < (cost12 + cost23) or (cost12 + cost31) < (cost23 + cost31):
      draw_final_path(ROOT, canvas, path12 + path31, graph)
      print("The number of explored nodes of Tri-directional Search:", explored_nodes12 + explored_nodes31)
      print("The whole path:", (path12 + path31[1:]))
      print("The length of the whole path:", len((path12 + path31[1:])))
      return (path12 + path31[1:]), (cost12 + cost31)
    return None

def tri_directional_helper(start, goal, graph, col, ROOT, canvas, heuristic=dist_heuristic):
    counter = 0
    if start == goal:
        return [start, goal], graph[4][start, goal]
    frontierF, frontierB, exploredF, exploredB = PriorityQueue(), PriorityQueue(), {start: "s"}, {goal: "f"}
    frontierF.push((heuristic(start, goal, graph), start, [start]))
    frontierB.push((heuristic(goal, start, graph), goal, [goal]))
    old_exploredF = []
    old_exploredB = []
    while frontierF or frontierB:
        poppedF = frontierF.pop()
        poppedB = frontierB.pop()
        current_pathF = poppedF[2]  # path
        current_pathB = poppedB[2]  # path
        current_nodeF = poppedF[1]
        current_nodeB = poppedB[1]
        costF = poppedF[0] - heuristic(current_nodeF, goal, graph)
        costB = poppedB[0] - heuristic(current_nodeB, start, graph)
        if current_nodeF == goal:  # current value
            pathF = current_pathF
            return pathF, costF, len(exploredF)
        if current_nodeB == start:  # current value
            pathB = current_pathB
            return pathB[::-1], costB, len(exploredB)
        if (current_nodeF not in old_exploredF):
            old_exploredF.append(current_nodeF)
            for neighbor in graph[3][current_nodeF]:  # graph[3] is neighbors
                if neighbor not in old_exploredF:
                    exploredF[neighbor] = current_nodeF
                    new_cost = costF + graph[4][current_nodeF, neighbor] + heuristic(neighbor, goal, graph)
                    frontierF.push((new_cost, neighbor, current_pathF + [neighbor]))
                    drawLine(canvas, *graph[5][current_nodeF], *graph[5][neighbor], col) 
        if (current_nodeB not in old_exploredB):
            old_exploredB.append(current_nodeB)
            for neighbor in graph[3][current_nodeB]:  # graph[3] is neighbors
                if neighbor not in old_exploredB:
                    exploredB[neighbor] = current_nodeB
                    new_cost = costB + graph[4][current_nodeB, neighbor] + heuristic(neighbor, start, graph)
                    frontierB.push((new_cost, neighbor, current_pathB + [neighbor]))
                    drawLine(canvas, *graph[5][current_nodeB], *graph[5][neighbor], col)
        counter += 1
        if counter % 100 == 0: ROOT.update()
    return None

def main():
    start, goal, third = input("Start city: "), input("Goal city: "), input("Third city for tri-directional: ")
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")  # Task 1

    cur_time = time.time()
    path, cost = bfs(graph[2][start], graph[2][goal], graph, 'yellow')  # graph[2] is city to node
    if path != None:
        display_path(path, graph)
    else:
        print("No Path Found.")
    print('BFS Path Cost:', cost)
    print('BFS duration:', (time.time() - cur_time))
    print()

    cur_time = time.time()
    path, cost = bi_bfs(graph[2][start], graph[2][goal], graph, 'green')
    if path != None:
        display_path(path, graph)
    else:
        print("No Path Found.")
    print('Bi-BFS Path Cost:', cost)
    print('Bi-BFS duration:', (time.time() - cur_time))
    print()

    cur_time = time.time()
    path, cost = a_star(graph[2][start], graph[2][goal], graph, 'blue')
    if path != None:
        display_path(path, graph)
    else:
        print("No Path Found.")
    print('A star Path Cost:', cost)
    print('A star duration:', (time.time() - cur_time))
    print()

    cur_time = time.time()
    path, cost = bi_a_star(graph[2][start], graph[2][goal], graph, 'orange')
    if path != None: display_path(path, graph)
    else: print ("No Path Found.")
    print ('Bi-A star Path Cost:', cost)
    print ("Bi-A star duration: ", (time.time() - cur_time))
    print ()

    print ("Tri-Search of ({}, {}, {})".format(start, goal, third))
    cur_time = time.time()
    path, cost = tri_directional(graph[2][start], graph[2][goal], graph[2][third], graph, 'pink')
    if path != None: display_path(path, graph)
    else: print ("No Path Found.")
    print ('Tri-A star Path Cost:', cost)
    print ("Tri-directional search duration:", (time.time() - cur_time))

    mainloop()  # Let TK windows stay still

if __name__ == '__main__':
    main()

''' Sample Output:
Start city: Charlotte
Goal city: Los Angeles
Third city for tri-directional: Chicago
The number of explored nodes of BFS: 19735
The whole path: ['3700421', '3700258', ..., '0600427', '0600316']
The length of the whole path: 243
['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
BFS Path Cost: 2965.7640233572088
BFS duration: 288.9429421424866

The number of explored nodes of Bi-BFS: 12714
The whole path: ['3700421', '3700258', ..., '0600427', '0600316']
The length of the whole path 243
['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
Bi-BFS Path Cost: 2965.4128704488785
Bi-BFS duration: 115.2277946472168

The number of explored nodes of A star: 7692
The whole path: ['3700421', '3700258', ..., '0600427', '0600316']
The length of the whole path 319
['Charlotte', 'Dallas', 'Tucson', 'Los Angeles']
A star Path Cost: 2419.9700735372285
A star duration: 61.220252990722656

The number of explored nodes of Bi-A star: 3163
The whole path: ['3700421', '3700258', ..., '0600427', '0600316']
The length of the whole path 319
['Charlotte', 'Fort Worth', 'Tucson', 'Los Angeles']
Bi-A star Path Cost: 2467.9566632692486
Bi-A star duration: 8.88722538948059

Tri-Search of (Charlotte, Los Angeles, Chicago)
The whole path: ['0600316', '0600427', ..., '3700258', '3700421']
The length of the whole path 381
['Los Angeles', 'Chicago', 'Charlotte']
Tri-A star Path Cost: 2760.516003492685
Tri-directional search duration: 22.166738271713257
----jGRASP: operation complete.
'''
