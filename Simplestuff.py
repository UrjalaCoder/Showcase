import math
class Vector2():
    def __init__(self, x=0, y=0):
        self.x, self.y = (x, y)

        deltaSquare = math.pow(self.x, 2) + math.pow(self.y, 2)
        # Norm refers to the "magnitude" of the vector
        self.norm = math.sqrt(deltaSquare)


    def unit(self):
        return (self / self.norm)

    # string representation:
    def __str__(self):
        return "[{}, {}]".format(self.x, self.y)

    # Addition -->
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtraction -->
    def __sub__(self, other):
        return self + ((-1) * other)

    # Equality -->
    def __eq__(self, other):
        (self.x == other.x and self.y == other.y)

    # Division by a number -->
    def __truediv__(self, other):
        if (isinstance(other, int) or isinstance(other, float) and other != 0):
            return Vector2(self.x / other, self.y / other)
        else:
            raise ArithmeticError("Division by zero or by non number value!")

    # Multiplication is element-wise -->
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def translate(self, newI, newJ):
        return (newI * self.x) + (newJ * self.y)

def test():
    vectorA = Vector2(3, 4)
    vectorB = Vector2(2, 3)
    print(vectorA.norm)
    print(vectorB.norm)
    addVector = vectorA + vectorB
    print(vectorA + vectorB)
    print(addVector.norm)

    vectorC = Vector2(1, 1)
    print(vectorC.translate(Vector2(0, 1), Vector2(-1, 0)))
test()
