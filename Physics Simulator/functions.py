import math

# Calculate the distance between two points using the pythagoream threorum
def Distance(p0, p1):
    dx = p1["x"] - p0["x"]
    dy = p1["y"] - p0["y"]
    return math.sqrt(dx * dx + dy * dy)