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
    def __init__(self, x, y, r=25):
        self.x = x
        self.y = y
        self.r = r
        self.selected = False
        self.color = (155,155,155)
        self.connections = []
        self.draw()

    def draw(self):
        if self.selected:
            pygame.draw.circle(screen, (155,0,0), (self.x, self.y), self.r + 3)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def contains(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2) <= self.r

    def connect(self, other):
        self.connections.append(other)
        other.connections.append(self)

    def __repr__(self):
        return "Vertex at ({}, {})".format(self.x, self.y)

# Class to represent an edge
class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.draw()

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y))

    def __repr__(self):
        return "Edge between {} and {}".format(self.v1, self.v2)


isRunning = True
done = False
# List of vertices
vertices = []
# Selected vertex
selectedVertex = None
clickedVertex = None
# List of edges
edges = []

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if selectedVertex is None:
                # If the user clicks on the screen, but not on a vertex, this creates a new vertex
                vertices.append(Vertex(event.pos[0], event.pos[1]))
                selectedVertex = vertices[-1]
                selectedVertex.selected = True
            # If the user clicks on a vertex, this connects the vertex to the selected vertex
            for v in vertices:
                if v is not selectedVertex:
                    if v.contains(event.pos[0], event.pos[1]):
                        if selectedVertex and v.selected == False:
                            selectedVertex.connect(v)
                            edges.append(Edge(selectedVertex, v))
                        else:
                            selectedVertex = v
                            selectedVertex.selected = True
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            # If the user clicks on the screen, but not on a vertex, this deselects the selected vertex
            if selectedVertex is not None:
                if not selectedVertex.contains(event.pos[0], event.pos[1]):
                    selectedVertex.selected = False
                    selectedVertex = None

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] == 1:
            # If the user is dragging a vertex, this moves the vertex
            if selectedVertex is not None:
                selectedVertex.x = event.pos[0]
                selectedVertex.y = event.pos[1]
    screen.fill((0,0,0))
    for v in vertices:
        v.draw()
    for e in edges:
        e.draw()
    pygame.display.flip()
    clock.tick(60)

# Close the window and quit.
pygame.quit()