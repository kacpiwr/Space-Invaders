from turtle import Turtle, Screen, ontimer, pen, pendown, screensize


def initTurtle():
    screen = Screen()
    screen.tracer(8, 25)
    screen.bgcolor('black')
    screen.setworldcoordinates(0, 0, 500, 500)
    return screen


class Vader:
    def __init__(self, screen, x, y, color="green"):
        self.screen = screen
        self.body = Turtle()
        self.body.penup()
        self.body.hideturtle()
        self.body.color(color)
        self.body.pensize(5)
        self.x = x
        self.y = y
        self.draw()

    def draw(self):
        self.body.clear()
        self.body.setpos(self.x, self.y)
        self.body.pendown()
        for number in range(2):
            self.body.forward(20)
            self.body.right(90)
            self.body.forward(10)
            self.body.right(90)
        self.body.penup()

    def isHit(self, x, y):
        if x >= self.x and x <= self.x + 20 and y >= self.y and y <= self.y + 10:
            self.body.clear()
            return 0
        else:
            return 2

    def moveRight(self):
        self.x = self.x + 2
        self.draw()

    def moveDown(self):
        self.y = self.y - 10

    def moveLeft(self):
        self.x = self.x - 2
        self.draw()


class Emperror(Vader):
    def __init__(self, screen, x, y, color="red"):
        super().__init__(screen, x, y, color)
        self.live = 2

    def isHit(self, x, y):
        if x >= self.x and x <= self.x + 20 and y >= self.y and y <= self.y + 10:
            print(self.live)
            if self.live > 1:
                self.live -= 1
                self.color = "green"
                self.body.color(self.color)
                return 1
            else:
                self.body.clear()
                return 0


        else:
            return 2


class VaderInc:
    def __init__(self, screen):
        self.screen = screen
        self.body = Turtle()
        self.body.penup()
        self.body.hideturtle()
        self.body.color("white")

        self.vaders_list = []
        self.incubate()
        self.direction_right = True
        self.hits = 0
        self.score()

        self.move()

    def check(self, x, y):
        for row in self.vaders_list:
            for vader in row:
                hitted = vader.isHit(x, y)
                if hitted == 0:
                    row.remove(vader)
                    self.hits += 1
                    self.score()
                    return True

                elif hitted == 1:
                    self.hits += 1
                    self.score()
                    return True
        return False

    def incubate(self):
        for i in range(3):
            row_list = []
            for j in range(5):
                if i == 2:
                    invader = Emperror(self.screen, (50 + 60 * j), (200 + 50 * i))

                else:
                    invader = Vader(self.screen, (50 + 60 * j), (200 + 50 * i))

                row_list.append(invader)

            self.vaders_list.append(row_list)

    def move(self):
        down = False
        finito = False
        if self.direction_right:
            last = [row[-1].x for row in self.vaders_list if row]
            if last:
                if max(last) >= 470:
                    self.direction_right = False
                    down = True
            else:
                finito = True
        else:
            first = [row[0].x for row in self.vaders_list if row]
            if first:
                if min(first) <= 0:
                    self.direction_right = True
                    down = True
            else:
                finito = True
        if not finito:
            for i in self.vaders_list:
                for j in i:
                    if down:
                        j.moveDown()
                    if self.direction_right:
                        j.moveRight()

                    else:
                        j.moveLeft()

            down = False
            self.screen.ontimer(self.move, 100)

    def score(self):
        self.body.setpos(250, 400)
        self.body.clear()
        if self.hits >= 20:
            self.body.write("WIN!!!", align="center", font=("Arial", 50, "bold"))
        else:

            self.body.write(f"SCORE: {self.hits}", align="center", font=("Arial", 20, "bold"))


class Bullet:
    def __init__(self, screen, x=250, y=250, color="white", vaders=None):
        self.screen = screen
        self.body = Turtle()
        self.body.penup()
        self.body.hideturtle()
        self.body.color(color)
        self.body.pensize(5)
        self.vaders = vaders

        self.lock = False

        self.X = x + 10
        self.Y = y

        self.fire()

    def draw(self):
        if not self.lock:
            self.lock = True
            self.body.setpos(self.X, self.Y)
            self.body.pendown()
            self.body.dot(10)
            self.body.penup()
            self.lock = False

    def fire(self):
        self.Y += 1
        self.body.clear()
        self.draw()

        if not self.vaders.check(self.X, self.Y):
            if self.Y <= 600:
                screen.ontimer(self.fire, 5)

        else:
            self.body.clear()


class Tank:
    def __init__(self, screen, color="white", vaders=None):
        self.screen = screen
        self.body = Turtle()
        self.body.penup()
        self.body.hideturtle()
        self.body.color(color)
        self.body.pensize(5)
        self.x = 250
        self.y = 10
        self.vaders = vaders
        self.draw()
        self.unlocked = True

    def draw(self):
        self.body.clear()
        self.body.setpos(self.x, self.y)
        self.body.pendown()
        for number in range(2):
            self.body.forward(5)
            self.body.right(90)
            self.body.forward(100)
            self.body.right(90)
        self.body.penup()

    def moveRight(self):
        self.x = self.x + 20
        self.draw()

    def moveLeft(self):
        self.x = self.x - 20
        self.draw()

    def unlock(self):
        self.unlocked = True

    def shoot(self):
        if self.unlocked:
            bullet = Bullet(screen, self.x, self.y, vaders=self.vaders)
            self.unlocked = False
            screen.ontimer(self.unlock, 400)


screen = initTurtle()
deathstar = VaderInc(screen)
tank = Tank(screen, vaders=deathstar)

screen.onkey(tank.moveLeft, "a")
screen.onkey(tank.moveRight, "d")
screen.onkey(tank.shoot, "space")

screen.listen()
screen.mainloop()