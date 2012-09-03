# Worms!

# Worms walk over a grid. Each time they walk over a grid position, they deepen it.

from math import sin, cos, radians

GRID_SIZE = 100
GRID_SCALE = 10

size(GRID_SIZE * GRID_SCALE, GRID_SIZE * GRID_SCALE)

# (x,y): intensity
GRID = {}

WORM_ANGLES = 1

def clamp(x, lower, upper):
    return min(max(x, lower), upper)

class Worm:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random(GRID_SIZE)
        self.y = random(GRID_SIZE)
        self.timer = random(100)
        self.angled = 0
        self.angle = random(int(360 / float(WORM_ANGLES))) * WORM_ANGLES
        

    def random_walk(self):
        vx = sin(radians(self.angle))
        vy = cos(radians(self.angle))
        self.x += vx
        self.y += vy
        self.x = clamp(self.x, 0, GRID_SIZE-1)
        self.y = clamp(self.y, 0, GRID_SIZE-1)
        if self.x <= 0 or self.x >= GRID_SIZE - 1 or self.x <= 0 or self.y >= GRID_SIZE:
            self.reset()
        self.angle += self.angled
        self.timer -= 1
        if self.timer <= 0:
            self.angled = random(-2.0, 2.0)
            self.timer = random(100)
                
    def turn_right(self):
        self.angle = (self.angle + WORM_ANGLES) % 360

    def turn_left(self):
        self.angle = (self.angle - WORM_ANGLES) % 360
        
        
    
    
worms = [Worm() for i in range(10)]

def dot(x, y):
    rect(x * GRID_SCALE, y * GRID_SCALE, GRID_SCALE, GRID_SCALE)
    
def mark_grid(grid, x, y):
    ix = int(round(x))
    iy = int(round(y))
    intensity = grid.get((ix, iy), 0)
    intensity += 1
    grid[(ix,iy)] = intensity

speed(100)

def draw():
    background(1)
    for i in range(100):
        for w in worms:
            w.random_walk()
            mark_grid(GRID, w.x, w.y)
        
    max_intensity = 100 # max(GRID.values())
    #print GRID
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            intensity = GRID.get((x, y), 0)
            fill((max_intensity - intensity)/float(max_intensity))
            dot(x, y)
    
    #print GRID