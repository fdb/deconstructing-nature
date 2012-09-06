supershape = ximport("supershape")

colorrange(255)
size(1000, 1000)
background(247,247,247)
nofill()
stroke(70,72,75)
strokewidth(0.8)
from random import seed
seed(21)

x, y = 500, 500
w, h = 20, 20

# Create base random shape
m = random(1, 200)
n1 = random(0.001, 200)
n2 = random(0.001, 200)
n3 = random(0.001, 200)
p = supershape.path(x, y, w, h, m, n1, n2, n3, points=100)
drawpath(p)

# Repeatedly apply supershapes on supershapes
for i in range(100):
    m = random(1, 200)
    n1 = random(0.001, 200)
    n2 = random(0.001, 200)
    n3 = random(0.001, 200)
    t = Transform()
    t.translate(x, y)
    t.scale(1.02)
    t.translate(-x, -y)
    p = t.transformBezierPath(p)
    p = supershape.transform(p, m, n1, n2, n3, points=100)
    drawpath(p)
