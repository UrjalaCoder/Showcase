import tkinter as tk
import math, random, time

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480

ANIMATION_RUNNING = False

class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def magnitude(self):
        deltaPow = math.pow(self.x, 2) - math.pow(self.y, 2)
        return math.sqrt(deltaPow)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    # Setting the GUI element of a single particle.
    def setGUI(self, gui):
        self.gui = gui

    def getGUI(self):
        return self.gui

    def move(self, canvas):
        self.position = self.position + self.velocity
        canvas.move(self.gui, self.velocity.x, self.velocity.y)
        if self.position.x + 5 > CANVAS_WIDTH or self.position.x < 0:
            self.velocity.x = self.velocity.x * (-1)
        if self.position.y + 5 > CANVAS_HEIGHT or self.position.y < 0:
            self.velocity.y = self.velocity.y * (-1)

# def updateAnimation(rootWindow, particles):

def generateParticles(amount):
    particles = []
    for i in range(amount):
        rx, ry = (random.randint(0, CANVAS_WIDTH - 1), random.randint(0, CANVAS_HEIGHT - 1))
        particle = Particle(Vector2(rx, ry))
        particles.append(particle)
    return particles

def stop(rootWindow, canvas):
    canvas.delete('all')
    global ANIMATION_RUNNING
    ANIMATION_RUNNING = False

def start(rootWindow, slider, canvas):
    global ANIMATION_RUNNING
    if ANIMATION_RUNNING:
        return
    ANIMATION_RUNNING = True
    amount = slider.get()
    particles = generateParticles(amount)
    # particles = [Particle(Vector2(1, 1))]
    for particle in particles:
        x2, y2 = (particle.position.x + 5, particle.position.y + 5)
        rect = canvas.create_rectangle(particle.position.x, particle.position.y, x2, y2)
        # print(rect)
        particle.setGUI(rect)

    # Main loop -->
    last_time = time.time()
    while ANIMATION_RUNNING:
        if time.time() - last_time > (1 / 60):
            for particle in particles:
                particle.move(canvas)
                canvas.update()
            last_time = time.time()
    # End of main loop

def initGUI(root):
    particleAmountSlider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
    particleAmountSlider.pack()

    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()
    # TODO: Canvas logic and stopping and starting the animation. Maybe object with GUI elements as properties and some logic to ease the function to function communication.

    tk.Button(root, text="Stop Animation", command=lambda: stop(root, canvas)).pack()
    tk.Button(root, text="Start Animation", command=lambda: start(root, particleAmountSlider, canvas)).pack()

def main():

    root = tk.Tk()
    initGUI(root)
    tk.mainloop()

if __name__ == "__main__":
    main()
