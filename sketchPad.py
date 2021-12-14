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
        self.connections = []
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
            return abs(y_intercept - y) <= self.width

    def __repr__(self):
        return "Edge between {} and {}".format(self.v1, self.v2)
""" 
# A similar class to Edge but it uses arcs instead of lines
class Arc:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v1.ID = v1.ID
        self.v2 = v2
        self.v2.ID = v2.ID
        self.width = 8
        self.selected = False
        self.draw()

    # Draw the arc using the midpoint algorithm
    def draw(self):
        # Update v1 and v2 from the vertices
        self.v1 = vertices[self.v1.ID]
        self.v2 = vertices[self.v2.ID]
        if self.v1.x == self.v2.x:
            x = self.v1.x
            y = self.v1.y + (self.v2.y - self.v1.y) / 2
            pygame.draw.arc(screen, (155,155,155), (x - self.width, y - self.width, self.width * 2, self.width * 2), 0, math.pi, self.width)
        elif self.v1.y == self.v2.y:
            x = self.v1.x + (self.v2.x - self.v1.x) / 2
            y = self.v1.y
            pygame.draw.arc(screen, (155,155,155), (x - self.width, y - self.width, self.width * 2, self.width * 2), math.pi / 2, math.pi * 3 / 2, self.width)
        else:
            # Calculate the midpoint of the edge
            x = (self.v1.x + self.v2.x) / 2
            y = (self.v1.y + self.v2.y) / 2
            # Calculate the slope
            m = (self.v2.y - self.v1.y) / (self.v2.x - self.v1.x)
            # Calculate the angle of the slope
            angle = math.atan(m)
            # Calculate the length of the arc
            length = math.sqrt((self.v2.x - self.v1.x)**2 + (self.v2.y - self.v1.y)**2)
            # Draw the arc
            pygame.draw.arc(screen, (155,155,155), (x - length/2 - self.width, y - length/2 - self.width, length + self.width * 2, length + self.width * 2), angle, angle + math.pi, self.width)


    def contains(self, x, y):
        # Check if the point is within the arc
        m = (self.v2.y - self.v1.y) / (self.v2.x - self.v1.x)
        b = self.v1.y - m * self.v1.x
        y_intercept = m * x + b
        return abs(y_intercept - y) <= self.width

    def __repr__(self):
        return "Arc between {} and {}".format(self.v1, self.v2) """
""" 
# A class that represents an arc that connects a vertex to itself
class SelfArc:
    def __init__(self, v):
        self.v = v
        self.v.ID = v.ID
        self.width = 5
        self.selected = False
        self.draw()

    def draw(self):
        # Update v from the vertex
        self.v = vertices[self.v.ID]
        x = self.v.x
        y = self.v.y
        # Draw the arc such that the full circle is drawn
        pygame.draw.arc(screen, (155,155,155), (x, y, 50, 50), 0, math.pi * 2, self.width)

    def contains(self, x, y):
        # Check if the point is within the arc
        m = 0
        b = self.v.y
        y_intercept = m * x + b
        return abs(y_intercept - y) <= self.width

    def __repr__(self):
        return "SelfArc at {}".format(self.v)
 """

# Function to rearrange the vertices so that they are more evenly spaced
def arrangeVertices(vertices):
    # Find the center of the polygon
    center_x = sum([v.x for v in vertices]) / len(vertices)
    center_y = sum([v.y for v in vertices]) / len(vertices)

    # Rearrange the vertices
    for v in vertices:
        x = v.x - center_x
        y = v.y - center_y
        theta = math.atan2(y, x)
        v.x = center_x + math.cos(theta) * 100
        v.y = center_y + math.sin(theta) * 100

# Return a list of all vertices that can be reached from the input vertex
def getReachableVertices(v, reachable):
    newReachable = reachable.copy()
    if v.ID not in newReachable:
        newReachable.append(v.ID)
        for c in v.connections:
            if c.ID not in newReachable:
                newReachable = getReachableVertices(c, newReachable)
    return newReachable



isRunning = True
done = False
font = pygame.font.SysFont("arial", 20)
# A list of 7 colors
colors = [(155,0,0), (0, 155, 0), (0, 0, 155), (155, 155, 0), (155, 0, 155), (0, 155, 155), (155, 155, 155)]
currColor = 0
# List of vertices
vertices = []
# List of reachable
currReachable = []
# Selected vertex
selection = None
# List of edges
edges = []
# List of components
components = []

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
        #         arrangeVertices(vertices)
        elif event.type == pygame.KEYDOWN:
             # If the delete key is pressed, check if the selection is a vertex or an edge, and delete it
            if event.key == pygame.K_DELETE:
                if selection is not None:
                    if isinstance(selection, Vertex):
                        # Delete the vertex and all edges connected to it
                        for vert in selection.connections:
                            vert.connections.remove(selection)
                        for edge in edges:
                            if edge.v1 == selection or edge.v2 == selection:
                                edges.remove(edge)
                        # Change the id of all vertices that have a higher id than the selected vertex to be one less
                        for v in vertices:
                            if v.ID > selection.ID:
                                v.ID -= 1
                        vertices.remove(selection)
                    elif isinstance(selection, Edge):
                        # Delete the edge and clear the connections of the vertices it connects
                        for vert in selection.v1.connections:
                            vert.connections.remove(selection.v2)
                        edges.remove(selection)
                    selection = None
            # If the L Keyis pressed and a vertex is selected, create a self loop
            elif event.key == pygame.K_l:
                if isinstance(selection, Vertex):
                    selection.connect(selection)
                    edges.append(Edge(selection, selection))
                    selection.selected = False
                    selection = None
            # If enter key pressed and a vertex is selected, update the reachable vertices
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                if isinstance(selection, Vertex):
                    currReachable = []
                    currReachable = getReachableVertices(selection, currReachable)
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
            if selection is not None:
                selection.x = event.pos[0]
                selection.y = event.pos[1]
        elif selection is not None:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
            """ # If the current selection is a vertex, and the user presses the L Key, create a self loop
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                if isinstance(selection, Vertex):
                    selection.connect(selection)
                    edges.append(Edge(selection))
                    selection.selected = False
                    selection = None """
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

    # Display the number of vertices as "n = number" in the top right corner
    vCount = font.render("n = {}".format(len(vertices)), True, (255,255,255))
    screen.blit(vCount, (screen.get_width() - vCount.get_width() - 10, 10))
    # Display the number of edges as "m = number" in the top right corner
    eCount = font.render("m = {}".format(len(edges)), True, (255,255,255))
    screen.blit(eCount, (screen.get_width() - eCount.get_width() - 10, 30))
    # Display the result of the getReachableVertices function in the top right corner
    reachableCount = font.render("Reachable: {}".format(currReachable), True, (255,255,255))
    screen.blit(reachableCount, (screen.get_width() - reachableCount.get_width() - 40, 50))

    
    pygame.display.flip()
    clock.tick(60)

# Close the window and quit.
pygame.quit()