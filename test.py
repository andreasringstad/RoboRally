class robot:
    register = ["a", "b", "c", "d", "e", "f"]
    pixelX = "x"
    pixelY = "y"
register = 3
robots = []
for i in range(2):
    robots.append(robot)
print(robots[0].register[register])
print(robots[0].pixelX)