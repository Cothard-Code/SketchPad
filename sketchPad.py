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
        self.width = 8
        self.selected = False
        self.draw()

    def draw(self):
        if self.selected:
            pygame.draw.line(screen, (155,0,0), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width + 3)
        pygame.draw.line(screen, (155,155,155), (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.width)

    def contains(self, x, y):
        # Check if the point is within the line segment
        m = (self.v2.y - self.v1.y) / (self.v2.x - self.v1.x)
        b = self.v1.y - m * self.v1.x
        y_intercept = m * x + b
        return abs(y_intercept - y) <= self.width

    def __repr__(self):
        return "Edge between {} and {}".format(self.v1, self.v2)


isRunning = True
done = False
# List of vertices
vertices = []
# Selected vertex
selection = None
# List of edges
edges = []

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # If the delete key is pressed, check if the selection is a vertex or an edge, and delete it
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                if selection is not None:
                    if isinstance(selection, Vertex):
                        # Delete the vertex and all edges connected to it
                        for edge in selection.connections:
                            edges.remove(edge)
                        vertices.remove(selection)
                    elif isinstance(selection, Edge):
                        selection.v1.connections.remove(selection.v2)
                        selection.v2.connections.remove(selection.v1)
                        edges.remove(selection)
                    selection = None
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] == 1:
            # If the user is dragging a vertex, this moves the vertex
            if selection is not None:
                selection.x = event.pos[0]
                selection.y = event.pos[1]
        elif selection is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if isinstance(selection, Vertex):
                    for v in vertices:
                        if v is not selection:
                            if v.contains(event.pos[0], event.pos[1]):
                                if selection and v.selected == False:
                                    selection.connect(v)
                                    edges.append(Edge(selection, v))
                                    """ selection.selected = False
                                    selection = None """
                            #break
                    selection.selected = False
                    selection = None
                elif isinstance(selection, Edge):
                    selection.selected = False
                    selection = None
                
                    
        elif selection is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
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
            """         elif event.type == pygame.MOUSEBUTTONUP:
            # If the user clicks on the screen, but not on a vertex, this deselects the selected vertex
            if selection is not None:
                if not selection.contains(event.pos[0], event.pos[1]):
                    selection.selected = False
                    selection = None """
        
    screen.fill((0,0,0))
    for e in edges:
        e.draw()
    for v in vertices:
        v.draw()
    
    pygame.display.flip()
    clock.tick(60)

# Close the window and quit.
pygame.quit()