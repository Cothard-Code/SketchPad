# Click empty space to draw a new vertex, click a vertex to select it, drag to move it. When a vertex is selected, click another vertex to connect it to the selected vertex

import pygame
import math
from pygame.locals import *
from random import randint

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
        self.draw()

    def draw(self):
        if self.isLoop:
            if self.selected:
                pygame.draw.circle(screen, (255,255,255), (self.v1.x, self.v1.y - 1.5*self.v1.r), 1.35*self.v1.r, math.floor(self.width/1.25 + 5))
            pygame.draw.circle(screen, (155,155,155), (self.v1.x, self.v1.y - 1.5*self.v1.r), 1.25*self.v1.r, math.floor(self.width/1.25))
        else:
            if self.selected:
                pygame.draw.line(screen, (255,255,255), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width + 2)
            pygame.draw.line(screen, (155,155,155), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width)
        
    def contains(self, x, y):
        # If self.isLoop, check if the point is on the circle
        if self.isLoop:
            dist = math.sqrt((self.v1.x - x)**2 + (self.v1.y - y - 1.5 * self.v1.r)**2)
            return dist >= self.v1.r and dist <= 1.25*self.v1.r

        # If not self.isLoop, check if the point is on the line
        else:
            m = (self.v2.y - self.v1.y) / (self.v2.x - self.v1.x)
            b = self.v1.y - m * self.v1.x
            y_intercept = m * x + b
            return abs(y_intercept - y) <= self.width and x >= min(self.v1.x, self.v2.x) and x <= max(self.v1.x, self.v2.x)

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

def dfs(v, visited, c):
    visited.append(v)
    c.append(v)
    for e in edges:
        if e.v1 == v and e.v2 not in visited:
            dfs(e.v2, visited, c)
        elif e.v2 == v and e.v1 not in visited:
            dfs(e.v1, visited, c)


# Function to determine if the graph is bipartite
def isBipartite(vertices, edges):
# Set the colors of all vertices to -1
    for v in vertices:
        v.color = -1
    # Set the colors of the first vertex to 0
    vertices[0].color = (155,0,0)
    # Set the colors of the second vertex to 1
    vertices[1].color = (0,0,155)
    # Set the colors of the rest of the vertices to the opposite of their neighbors' colors
    for v in vertices[2:]:
        for e in edges:
            if e.v1 == v:
                if e.v2.color == -1 and v.color == (155,0,0):
                    e.v2.color = (0,0,155)
                elif e.v2.color == -1 and v.color == (0,0,155):
                    e.v2.color = (155,0,0)
                elif e.v2.color == v.color:
                    return False
            elif e.v2 == v:
                if e.v1.color == -1 and v.color == (155,0,0):
                    e.v1.color = (0,0,155) - e.v1.color
                elif e.v1.color == -1 and v.color == (0,0,155):
                    e.v1.color = (155,0,0) - e.v1.color
                elif e.v1.color == v.color:
                    return False
    return True


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
# Bipartite Flag
bipartiteFlag = False

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
        #         arrangeVertices(vertices)
        elif event.type == pygame.KEYDOWN:
            # If the user presses the spacebar, then toggle bipartiteFlag
            if event.key == pygame.K_SPACE:
                bipartiteFlag = not bipartiteFlag
            # If the delete key is pressed, check if the selection is a vertex or an edge, and delete it
            if event.key == pygame.K_DELETE:
                if isinstance(selection, Vertex):
                    for edge in edges:
                        if edge.v1 == selection or edge.v2 == selection:
                            edges.remove(edge)
                    # Change the id of all vertices that have a higher id than the selected vertex to be one less
                    # May be breaky break
                    for v in vertices:
                        if v.ID > selection.ID:
                            v.ID -= 1
                    vertices.remove(selection)
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
        sDisplay = font.render("Vertex ID = {}".format(selection.ID), True, (255,255,255))
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
    if len(vertices) > 1:
        if bipartiteFlag == True:
            bipartiteDisplay = font.render("Bipartite = {}".format(isBipartite(vertices, edges)), True, (255,255,255))
        else:
            bipartiteDisplay = font.render("Bipartite = Unknown", True, (255,255,255))
        screen.blit(bipartiteDisplay, (screen.get_width() - bipartiteDisplay.get_width() - 10, 90))

    # Display the result of connectedComponents function in the top left corner
    if len(vertices) > 0:
        componentsList = connectedComponents(vertices, edges)
        ccCount = font.render("Connected Components: {}".format(componentsList), True, (255,255,255))
        screen.blit(ccCount, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Close the window and quit.
pygame.quit()