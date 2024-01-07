import math
def get_direction(x1,x2,y1,y2):
    deltaX = x1-x2
    deltaY = y1-y2
    rad = math.atan2(deltaX, deltaY)
    return math.sin(rad), math.cos(rad)

def normalize(value, min, max):
    return (value-min)/(max-min)

def distance(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1-x2, 2)+ math.pow(y1-y2,2))
