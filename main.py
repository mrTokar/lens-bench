from tkinter import Tk, Canvas, Frame
from tkinter import BOTH
from math import tan, radians

def solution_of_the_equation(k, point) -> tuple:
    '''Решает уравние вида y=kx + b по заданной точке для нахождения b
    Возвращает (k, b), где b = y - kx'''
    return (k, point[1] - k * point[0])

class Lens:
    def __init__(self, canvas, x, y, F):
        self.up = y # y-координата верха линзы
        self.center = (x, y+87.5) 
        self.down = y+175 # y-координата низа линзы
        self.F = self.center[0] + F
        canvas.create_line(x, self.up, x, self.down) # сохдание линзы
        # ----- оформление линзы ------ 
        canvas.create_line((x - 10, self.up + 10), (x, self.up), (x + 10, self.up + 10))
        canvas.create_line((x - 10, self.down - 10), (x, self.down), (x + 10, self.down - 10))

    def get_intersection(self, y= None, line= None):
        '''Находит точку пересечения лазера с линзой
        Если передан аргуемент y (Наколько выше центра падает лазер), то считает по нему
        Если передан аргумент line (ур-е прямой), то находит точку пересечения с помощьею него '''
        if y:
            return (self.center[0], self.center[1]-y)
        if line:
            return (self.center[0], line[0] * self.center[0] + line[1])

    def refraction_lazer(self, line, point):
        '''Вычисляет и возвращает ур-е приломленной прямой'''
        side_axis = solution_of_the_equation(line[0], self.center) # побочная оптическая ось
        f1 = side_axis[0] * self.F + side_axis[1] # f1 = k*F + b, проекция на ось y побочного фокуса
        k = (point[1] - f1)/(point[0] - self.F) # k = (ya - yf)/(xa - xf)
        line = solution_of_the_equation(k, point)
        return (line[0], line[1], (self.F, f1))


class Example(Frame):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.master.title("Скамья линз")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)

        lenses = []
        pad_x = 40
        pad_y = 10
        l = int(input("L в мм: ")) * 5
        f = int(input("F в мм: ")) * 5
        for _ in range(int(input("N: "))):
            lenses.append(Lens(self.canvas, pad_x, pad_y, f))
            pad_x += l

        for i in range(len(lenses)):
            if i == 0:
                pointA = lenses[0].get_intersection(y= int(input("y в мм: ")) * 5)
                a = int(input("a в градусах: ")) #alpha
                old_lazer = solution_of_the_equation(-tan(radians(a)), pointA) # (k, b) for y = kx + b
                self.canvas.create_line((0, old_lazer[1]), pointA, fill='red') # рисовка запускаемого лазера
            new_lazer = lenses[i].refraction_lazer(old_lazer, pointA)
            # если в скамье есть еще линзы, то рисуем лазер до нее, иначе до фокуса линзы
            if i + 1 <= len(lenses)-1:
                pointB = lenses[i+1].get_intersection(line=new_lazer)
                # если лазер попадает в линзу
                if lenses[i+1].up <= pointB[1] <= lenses[i+1].down: 
                    self.canvas.create_line(pointA, pointB, fill='red')
                    pointA, pointB = pointB, (0,0)
                    old_lazer = new_lazer
                else:
                    self.canvas.create_line(pointA, new_lazer[2], fill='red')
                    break
        else:
            self.canvas.create_line(pointA, new_lazer[2], fill='red')

        self.canvas.create_line((0, lenses[-1].center[1]), (lenses[-1].F, lenses[-1].center[1]), dash= (10, 5))
        self.canvas.pack(fill=BOTH, expand=1)
 
 
def main():
    root = Tk()
    ex = Example()
    root.geometry("1000x400")
    root.mainloop()
 
 
if __name__ == '__main__':
    main()
