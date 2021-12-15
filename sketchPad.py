# Click empty space to draw a new vertex, click a vertex to select it, drag to move it. When a vertex is selected, click another vertex to connect it to the selected vertex

import pygame
import math
import numpy as np
from collections import deque
from pygame.locals import *
from random import randint
import numpy as np


pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
pygame.display.set_caption("SketchPad")



# Class to represent a vertex
class Vertex:
    def __init__(self, x, y, r=25,):
        self.ID = len(vertices)
        self.x = x
        self.y = y
        self.r = r
        self.selected = False
        self.color = colors[currColor]
        self.draw()

    def draw(self):
        if self.selected:
            pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.r + 2)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        #draw the ID of the vertex on top of the vertex
        font = pygame.font.SysFont("Arial", 15)
        text = font.render(str(self.ID), True, (255,255,255))
        screen.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

    def contains(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2) <= self.r

    def __repr__(self):
        return "V{}".format(self.ID)

# Class to represent an edge
class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        # self.ID is composed of the IDs of the vertices from smallest to largest
        self.ID = "{} {}".format(min(v1.ID, v2.ID), max(v1.ID, v2.ID))
        self.width = 8
        self.selected = False
        # self.isLoop is true if self.v1 == self.v2
        self.isLoop = self.v1 == self.v2
        self.isBridge = False
        self.draw()

    def draw(self):
        if self.isLoop:
            if self.selected:
                pygame.draw.circle(screen, (255,255,255), (self.v1.x, self.v1.y - 1.5*self.v1.r), 1.35*self.v1.r, math.floor(self.width/1.25 + 5))
            pygame.draw.circle(screen, self.color, (self.v1.x, self.v1.y - 1.5*self.v1.r), 1.25*self.v1.r, math.floor(self.width/1.25))
        else:
            if self.selected:
                pygame.draw.line(screen, (255,255,255), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width + 2)
            if self.isBridge:
                pygame.draw.line(screen, (0,255,200), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width + 2)
            else:
                pygame.draw.line(screen, (155,155,155), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width)

            # if self.isBridge:
            #     pygame.draw.line(screen, (0,200,100), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width)
            # else:
            #     pygame.draw.line(screen, self.color, (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width)
        
    def contains(self, x, y):
        # If self.isLoop, check if the point is on the circle
        if self.isLoop:
            dist = math.sqrt((self.v1.x - x)**2 + (self.v1.y - y - 1.5 * self.v1.r)**2)
            return dist >= self.v1.r and dist <= 1.25*self.v1.r

        # If not self.isLoop, check if the point is on the line
        else:
            # Catch divide by zero error
            # Catch the case where the line is vertical
            if self.v1.x == self.v2.x:
                return self.v1.x == x and (self.v1.y - y) <= self.width and (self.v2.y - y) <= self.width   
            try:
                m = (self.v2.y - self.v1.y) / (self.v2.x - self.v1.x)
                b = self.v1.y - m * self.v1.x
                y_intercept = m * x + b
                return abs(y_intercept - y) <= self.width and x >= min(self.v1.x, self.v2.x) and x <= max(self.v1.x, self.v2.x)
            except ZeroDivisionError:
                m = (self.v2.y - self.v1.y) / (self.v2.x - self.v1.x + 30)
                b = self.v1.y - m * self.v1.x
                y_intercept = m * x + b
                return abs(y_intercept - y) <= self.width and x >= min(self.v1.x, self.v2.x) and x <= max(self.v1.x, self.v2.x)

    def setIsBridge(self):
        self.isBridge = True

    def setIsNotBridge(self):
        self.isBridge = False

    def __repr__(self):
        return "Edge between {} and {}".format(self.v1, self.v2)
  

# Function to decompose the graph into a list of connected components
def connectedComponents(vertices, edges):
    visited = []
    components = []
    for v in vertices:
        if v not in visited:
            c = []
            dfs(v, visited, c)
            components.append(c)
    return components

# Depth-first search to find the connected component of a vertex
def dfs(v, visited, c):
    visited.append(v)
    c.append(v)
    for e in edges:
        if e.v1 == v and e.v2 not in visited:
            dfs(e.v2, visited, c)
        elif e.v2 == v and e.v1 not in visited:
            dfs(e.v1, visited, c)

# Custom DFS function to find bridges
def dfs2(v, o, u, visited, c):
    visited.append(v)
    c.append(v)
    for e in edges:
        if not(e.v1 == o and e.v2 == u) and not(e.v1 == u and e.v2 == 0):
            if e.v1 == v and e.v2 not in visited:
                dfs2(e.v2, o, u, visited, c)
            elif e.v2 == v and e.v1 not in visited:
                dfs2(e.v1, o, u, visited, c)

# Check is the edge is a bridge
def checkBridge(e, vertices, edges):
    v = e.v1
    o = e.v1
    u = e.v2
    visited = []
    c = []
    dfs(u, visited, c)
    firstC = len(visited)
    visited = []
    #edges.remove(e)
    dfs2(v, o, u, visited, c)
    if len(visited) == firstC:
        return False
    else:
        return True

# Function to determine if the graph can be divided into two partitions, and return them
def getPartitions(vertices, edges):
    q = deque()
    partition1 = set()
    partition2 = set()
    dist = {}
    for v in vertices:
        if v not in dist:
            dist[v] = 0
            q.append(v)
            partition1.add(v)
            try:
                while True:
                    v = q.pop()
                    # Add all neighbors of v to the neighbors list
                    neighbors = []
                    for e in edges:
                        if e.v1 == v:
                            neighbors.append(e.v2)
                        elif e.v2 == v:
                            neighbors.append(e.v1)
                    for w in neighbors:
                        if w not in dist:
                            dist[w] = dist[v] + 1
                            q.append(w)
                            if dist[w] % 2 == 0:
                                partition1.add(w)
                            else:
                                partition2.add(w)
                        else:
                            if (dist[w] + dist[v]) % 2 == 0:
                                return set(), set()
            except:
                pass
    return partition1, partition2
                
# Function to determine if the graph is bipartite
def isBipartite(vertices, edges):
    partition1, partition2 = getPartitions(vertices, edges)
    if len(connectedComponents(vertices, edges)) > 1:
        return False
    return len(partition1) > 0 and len(partition2) > 0

# Function to produce an adjacency matrix for the graph [DONE]
def getAdjacencyMatrix(vertices, edges):
    adjacencyMatrix = [[0 for i in range(len(vertices))] for j in range(len(vertices))]
    for e in edges:
        adjacencyMatrix[e.v1.ID][e.v2.ID] = 1
        adjacencyMatrix[e.v2.ID][e.v1.ID] = 1
    return adjacencyMatrix

# Function to produce the degree matrix for the graph [DONE]
def getDegreeMatrix(vertices, edges):
    degreeMatrix = [[0 for i in range(len(vertices))] for j in range(len(vertices))]
    for e in edges:
        degreeMatrix[e.v1.ID][e.v1.ID] += 1
        degreeMatrix[e.v2.ID][e.v2.ID] += 1
    return degreeMatrix

# Function to produce Laplacian matrix for the graph [DONE]
def getLaplacianMatrix(vertices, edges):
    degreeMatrix = getDegreeMatrix(vertices, edges)
    adjacencyMatrix = getAdjacencyMatrix(vertices, edges)
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            degreeMatrix[i][j] = degreeMatrix[i][j] - adjacencyMatrix[i][j]
    return degreeMatrix

# Function to produce the eigenvalues and eigenvectors of the Laplacian matrix [DONE]
def getEigenvalues(vertices, edges):
    laplacianMatrix = getLaplacianMatrix(vertices, edges)
    eigenvalues, eigenvectors = np.linalg.eig(laplacianMatrix)
    return eigenvalues, eigenvectors

# Function that implements Dijkstra's algorithm to find the shortest path between two vertices [UNTESTED]
def dijkstra(vertices, edges, start, end):
    dist = {}
    prev = {}
    for v in vertices:
        dist[v] = float('inf')
        prev[v] = None
    dist[start] = 0
    q = deque()
    q.append(start)
    while len(q) > 0:
        u = q.pop()
        for e in edges:
            if e.v1 == u and e.v2 not in dist:
                dist[e.v2] = dist[u] + 1
                prev[e.v2] = u
                q.append(e.v2)
            elif e.v2 == u and e.v1 not in dist:
                dist[e.v1] = dist[u] + 1
                prev[e.v1] = u
                q.append(e.v1)
    if dist[end] == float('inf'):
        return []
    path = []
    u = end
    while u != None:
        path.append(u)
        u = prev[u]
    path.reverse()
    return path

# Function to generate a graph from an adjacency matrix [DONE]
def generateGraph(adjacencyMatrix):
    vertices = []
    edges = []
    for i in range(len(adjacencyMatrix)):
        vertices.append(Vertex(i))
    for i in range(len(adjacencyMatrix)):
        for j in range(len(adjacencyMatrix)):
            if adjacencyMatrix[i][j] == 1:
                edges.append(Edge(vertices[i], vertices[j]))
    return vertices, edges

# Function to generate a graph that is a grid of size n x n [DONE]
def generateGrid(n):
    vertices = []
    edges = []
    for i in range(n):
        for j in range(n):
            v = Vertex((i*15)*n + 100, j*15*n + 100)
            v.ID = len(vertices)
            vertices.append(v)
    for i in range(n):
        for j in range(n):
            if i < n - 1:
                edges.append(Edge(vertices[i*n + j], vertices[(i+1)*n + j]))
            if j < n - 1:
                edges.append(Edge(vertices[i*n + j], vertices[i*n + j + 1]))
    return vertices, edges

# Function to generate a graph that is a cycle of size n [DONE]
def generateCycle(n):
    vertices = []
    edges = []
    for i in range(n):
        v = Vertex(300 + (math.cos(i*2*math.pi/n)*200), 300 + (math.sin(i*2*math.pi/n)*200))
        v.ID = len(vertices)
        vertices.append(v)
    for i in range(n):
        edges.append(Edge(vertices[i], vertices[(i+1)%n]))
    return vertices, edges

# Function to generate a graph that is a star of size n [DONE]
def generateStar(n):
    vertices = []
    edges = []
    for i in range(n):
        v = Vertex(300 + (math.cos(i*2*math.pi/n)*200), 300 + (math.sin(i*2*math.pi/n)*200))
        v.ID = len(vertices)
        vertices.append(v)
    for i in range(n):
        edges.append(Edge(vertices[i], vertices[(i+1)%n]))
    for i in range(n):
        edges.append(Edge(vertices[i], vertices[(i+2)%n]))
    return vertices, edges

# Function to determine if the graph is a grid structure [Not working]
def isGrid(vertices, edges):
    degreeMatrix = getDegreeMatrix(vertices, edges)
    for i in range(1,len(vertices)-1):
        if degreeMatrix[i][i] != 4:
            return False
    return True

# Function to move vertices to the center of the grid [Just an idea]
def beautifyGraph(vertices, edges):
    if isGrid(vertices, edges):
        print("Graph is a grid")
        x = 0
        y = 0
        for v in vertices:
            x += v.x
            y += v.y
        x /= len(vertices)
        y /= len(vertices)
        for v in vertices:
            v.x -= x
            v.y -= y
    else:
        print("Graph does not have an obvious structure")

# Function to save the graph to a file [DONE]
def saveGraph(vertices, edges, filename):
    with open(filename, 'w') as f:
        for v in vertices:
            f.write("v " + str(v.x) + " " + str(v.y) + "\n")
        for e in edges:
            f.write("e " + str(e.v1.ID) + " " + str(e.v2.ID) + "\n")

# Function to load a graph from a file [DONE]
def loadGraph(filename):
    vertices = []
    edges = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'v':
                x = float(line.split()[1])
                y = float(line.split()[2])
                v = Vertex(x, y)
                v.ID = len(vertices)
                vertices.append(v)
            elif line[0] == 'e':
                v1 = vertices[int(line.split()[1])]
                v2 = vertices[int(line.split()[2])]
                e = Edge(v1, v2)
                edges.append(e)
    return vertices, edges

isRunning = True
done = False
font = pygame.font.SysFont("arial", 20)
# A list of 7 colors
colors = [(155,0,0), (0, 155, 0), (0, 0, 155), (155, 155, 0), (155, 0, 155), (0, 155, 155), (155, 155, 155)]
currColor = 0
# List of vertices
vertices = []
# Selection
selection = None
# List of edges
edges = []
# List of connected components
componentsList = []

# Graph Presets
#vertices, edges = generateGrid(5)
#vertices, edges = generateCycle(10)
#vertices, edges = generateStar(5)
# Main loop

while not done:
    for e in edges:
        if e.isBridge:
            e.setIsNotBridge()
        if checkBridge(e, vertices, edges):
            e.setIsBridge()
        else:
            e.setIsNotBridge()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # if the user pressed ctrl+s, save the graph
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Prompt the user for a filename
                filename = input("Enter a filename: ")
                saveGraph(vertices, edges, filename)
            # if the user pressed ctrl+o, load a graph
            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Prompt the user for a filename
                filename = input("Enter a filename: ")
                vertices, edges = loadGraph(filename)
            # If the user presses the m key, print the adjacency matrix, degree matrix, and laplacian matrix
            if event.key == pygame.K_m:
                adjacencyMatrix = getAdjacencyMatrix(vertices, edges)
                print("Adjacency Matrix:")
                for i in range(len(adjacencyMatrix)):
                    print(adjacencyMatrix[i])
                print("")
                degreeMatrix = getDegreeMatrix(vertices, edges)
                print("Degree Matrix:")
                for i in range(len(degreeMatrix)):
                    print(degreeMatrix[i])
                print("")
                laplacianMatrix = getLaplacianMatrix(vertices, edges)
                print("Laplacian Matrix:")
                for i in range(len(laplacianMatrix)):
                    print(laplacianMatrix[i])
                print("")
            # If the user pressed the b key, the graph is beautified [BROKEN]
            elif event.key == pygame.K_b:
                beautifyGraph(vertices, edges)
            # If the delete key is pressed, check if the selection is a vertex or an edge, and delete it
            elif event.key == pygame.K_DELETE:
                if isinstance(selection, Vertex):
                    # For every edge, check if the vertex is in the edge and delete the edge if it is
                    for e in edges:
                        if e.v1 == selection or e.v2 == selection:
                            edges.remove(e)
                    vertices.remove(selection)
                    # Change the id of all vertices that have a higher id than the selected vertex to be one less
                    for v in vertices:
                        if v.ID > selection.ID:
                            v.ID -= 1
                elif isinstance(selection, Edge):
                    # Delete the edge
                    edges.remove(selection)
                selection = None
            # If the L key is pressed and a vertex is selected, create a self loop
            elif event.key == pygame.K_l:
                if isinstance(selection, Vertex):
                    # Check if the vertex already has a self loop
                    alreadyLooped = False
                    for e in edges:
                        if e.ID == "{} {}".format(selection.ID, selection.ID):
                            alreadyLooped = True
                    if not alreadyLooped:
                        edges.append(Edge(selection, selection))
                        selection.selected = False
                        selection = None
            # If the left arrow key is pressed, change the curr Color to the previous color and set the color of the selected vertex to the previous color
            # If the currColor is 0, set it to the last color in the list
            elif event.key == pygame.K_LEFT:
                # If selection is a vertex
                if isinstance(selection, Vertex):
                    currColor -= 1
                    if currColor < 0:
                        currColor = len(colors) - 1
                    selection.color = colors[currColor]
            # If the right arrow key is pressed, change the curr Color to the next color and set the color of the selected vertex to the next color
            # If the currColor is the last color in the list, set it to 0
            elif event.key == pygame.K_RIGHT:
                # If selection is a vertex
                if isinstance(selection, Vertex):
                    currColor += 1
                    if currColor >= len(colors):
                        currColor = 0
                    selection.color = colors[currColor]
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] == 1:
            # If the user is dragging a vertex, this moves the vertex
            if isinstance(selection, Vertex):
                selection.x = event.pos[0]
                selection.y = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if isinstance(selection, Vertex):
                for v in vertices:
                    if v is not selection:
                        if v.contains(event.pos[0], event.pos[1]):
                            # If there is not already an edge between the two vertices, create one
                            alreadyConnected = False
                            for e in edges:
                                if (e.v1.ID == selection.ID and e.v2.ID == v.ID) or (e.v1.ID == v.ID and e.v2.ID == selection.ID):
                                    alreadyConnected = True
                                    break
                            if not alreadyConnected:
                                edges.append(Edge(selection, v))
                                break
                selection.selected = False
                selection = None
            elif isinstance(selection, Edge):
                selection.selected = False
                selection = None
            else:
                for v in vertices:
                    if v.contains(event.pos[0], event.pos[1]):
                        selection = v
                        selection.selected = True
                if selection is None:
                    for e in edges:
                        if e.contains(event.pos[0], event.pos[1]):
                            selection = e
                            selection.selected = True
                if selection is None:
                    vertices.append(Vertex(event.pos[0], event.pos[1]))
                    selection = vertices[-1]
                    selection.selected = True

    screen.fill((0,0,0))
    for e in edges:
        e.draw()
    for v in vertices:
        v.draw()

    # Display the number of vertices as "n = number" in the top right corner
    vCount = font.render("n = {}".format(len(vertices)), True, (255,255,255))
    screen.blit(vCount, (screen.get_width() - vCount.get_width() - 10, 10))

    # Display the number of edges as "m = number" in the top right corner
    eCount = font.render("m = {}".format(len(edges)), True, (255,255,255))
    screen.blit(eCount, (screen.get_width() - eCount.get_width() - 10, 30))

    # If the user has selected a vertex, display the vertex's ID as "Vertex ID = number" in the top right corner.
    # If the user has selected an edge, display the edge's ID as "Edge ID = number"
    # If the user has selected nothing, display "Selection Empty."
    if isinstance(selection, Vertex):
        sDisplay = font.render("Vertex ID = {}".format(selection.ID), True, (255,255,255))
    elif isinstance(selection, Edge):
        sDisplay = font.render("Edge ID = {}".format(selection.ID), True, (255,255,255))
    else:
        sDisplay = font.render("Selection Empty", True, (255,255,255))
    screen.blit(sDisplay, (screen.get_width() - sDisplay.get_width() - 10, 50))

    # If the user has selected a vertex, display the degree of the selected vertex as "Degree = number" in the top right corner
    if isinstance(selection, Vertex):
        # Count the number of edges connected to the vertex
        degree = 0
        for e in edges:
            if e.v1 == selection or e.v2 == selection:
                if e.v1 == selection and e.v2 == selection:
                    degree += 2
                else:
                    degree += 1
        degreeDisplay = font.render("Degree = {}".format(degree), True, (255,255,255))
        screen.blit(degreeDisplay, (screen.get_width() - degreeDisplay.get_width() - 10, 70))

    # Display the result of isBipartite() as "Bipartite = True/False" in the top right corner
    # Display the result of getPartitions() as "Partitions = [list of lists]" in the top right corner
    if len(vertices) > 1:
        bipartiteDisplay = font.render("Bipartite = {}".format(isBipartite(vertices, edges)), True, (255,255,255))
        partitionsDisplay = font.render("Partitions = {}".format(getPartitions(vertices, edges)), True, (255,255,255))
    else:
        bipartiteDisplay = font.render("Bipartite = Unknown", True, (255,255,255))
        partitionsDisplay = font.render("Partitions = Unknown", True, (255,255,255))
    screen.blit(bipartiteDisplay, (screen.get_width() - bipartiteDisplay.get_width() - 10, 90))
    screen.blit(partitionsDisplay, (screen.get_width() - partitionsDisplay.get_width() - 10, 110))

    # Display the result of connectedComponents function in the top left corner
    # and the number of CCs
    if len(vertices) > 0:
        componentsList = connectedComponents(vertices, edges)
        numComponents = len(componentsList)
        ccTitle = font.render("List of Connected Components:", True, (255,255,255))
        ccList = font.render("{}".format(componentsList), True, (255,255,255))
        ccNum = font.render("Number of CCs: {}".format(numComponents), True, (255,255,255))
        screen.blit(ccTitle, (10, 10))
        screen.blit(ccList, (10, 30))
        screen.blit(ccNum, (10, 50))

    pygame.display.flip()
    clock.tick(60)

# Close the window and quit.
pygame.quit()