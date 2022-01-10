# Running some rope simulation using Tkinter and Pygame. Seems like it'd be a fun thing to do.
from pygame import rect
from functions import *
import math
import pygame
from pygame.draw import circle

pygame.init()
pygame.font.init()

# Set up the screen
backgroundColor = (56, 108, 117)
(width, height) = (800, 600)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Physics")

# General Variables
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
dt = clock.tick(60)

points = []
sticks = []
forms = []

points.append({
    "x": 100,
    "y": 100,
    "oldx": 80,
    "oldy": 95
})
points.append({
    "x": 200,
    "y": 100,
    "oldx": 200,
    "oldy": 100
})
points.append({
    "x": 200,
    "y": 200,
    "oldx": 200,
    "oldy": 200
})
points.append({
    "x": 100,
    "y": 200,
    "oldx": 100,
    "oldy": 200
})

sticks.append({
    "p0": points[0],
    "p1": points[1],
    "length": Distance(points[0],points[1]),
    "hidden": False
})
sticks.append({
    "p0": points[1],
    "p1": points[2],
    "length": Distance(points[1],points[2]),
    "hidden": False
})
sticks.append({
    "p0": points[2],
    "p1": points[3],
    "length": Distance(points[2],points[3]),
    "hidden": False
})
sticks.append({
    "p0": points[3],
    "p1": points[0],
    "length": Distance(points[3],points[0]),
    "hidden": False
})
sticks.append({
    "p0": points[0],
    "p1": points[2],
    "length": Distance(points[0],points[2]),
    "hidden": True
})

# Physics Variables
circleRadius = 7.5
stickWidth = 7.5
maxVelocity = 5
bounce = 0.9
gravity = 0.5
friction = 0.999

# main function, duh
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
        Render()

# Update all the points based off of forces
def UpdatePoints():
    for point in range(points.__len__()):
        p = points[point]
        vx = (p["x"] - p["oldx"]) * friction
        vy = (p["y"] - p["oldy"]) * friction

        p["oldx"] = p["x"]
        p["oldy"] = p["y"]
        p["x"] += vx
        p["y"] += vy
        p["y"] += gravity

# Constrain the points to within the screen
def ConstrainPoints():
    for point in range(points.__len__()):
        p = points[point]
        vx = (p["x"] - p["oldx"]) * friction
        vy = (p["y"] - p["oldy"]) * friction
        
        # Change direction when it hits the border.
        if p["x"] > width - circleRadius:
            p["x"] = width - circleRadius
            p["oldx"] = p["x"] + vx * bounce
        elif p["x"] < 0 + circleRadius:
            p["x"] = 0 + circleRadius
            p["oldx"] = p["x"] + vx * bounce

        if p["y"] > height - circleRadius:
            p["y"] = height - circleRadius
            p["oldy"] = p["y"] + vy * bounce
        elif p["y"] < 0 + circleRadius:
            p["y"] = 0 + circleRadius
            p["oldy"] = p["y"] + vy * bounce

# Move the points to a position where the stick is happy
def UpdateSticks():
    for stick in sticks:
        dx = stick["p1"]["x"] - stick["p0"]["x"]
        dy = stick["p1"]["y"] - stick["p0"]["y"]
        distance = math.sqrt(dx * dx + dy * dy)
        difference = stick["length"] - distance
        percent = difference / distance / 2
        offsetX = dx * percent
        offsetY = dy * percent

        stick["p0"]["x"] -= offsetX
        stick["p0"]["y"] -= offsetY
        stick["p1"]["x"] += offsetX
        stick["p1"]["y"] += offsetY

# Loop through the points and draw them on screen
def RenderPoints():
    for point in range(points.__len__()):
        p = points[point]
        pygame.draw.circle(surface=screen, color=(0,0,0), radius=circleRadius, center=(p["x"], p["y"]))

def RenderSticks():
    for stick in sticks:
        if stick["hidden"] != True:
            pygame.draw.line(surface=screen, color=(0,0,0), start_pos=(stick["p0"]["x"], stick["p0"]["y"]), end_pos=(stick["p1"]["x"], stick["p1"]["y"]), width=math.floor(stickWidth))

# Return a variable with the fps
def UpdateFPS():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color(0,0,0))
    return fps_text

# Call all necessary functions to render things within the screen
def Render():
    screen.fill(backgroundColor)
    UpdatePoints()
    for i in range(3): # Run multiple times for more stable physics calculations
        UpdateSticks()
        ConstrainPoints()
    # RenderPoints()
    RenderSticks()
    screen.blit(source=UpdateFPS(), dest=[3,0])
    pygame.display.update()    

if __name__ == "__main__":
    main()