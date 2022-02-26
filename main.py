from cmath import atan, pi
from tkinter import Label, Tk, Canvas, Frame, Scrollbar
from tkinter import BOTH, HORIZONTAL, ALL, NW, N, W
from math import tan, radians, atan, pi

def solution_of_the_equation(k, point) -> tuple:
    '''Решает уравние вида y=kx + b по заданной точке для нахождения b
    Возвращает (k, b), где b = y - kx'''
    return (k, point[1] - k * point[0])

class Lens:
    def __init__(self, canvas, x, y, F, number):
        l = 35 * 5 # длинна линзы
        self.up = y # y-координата верха линзы
        self.center = (x, y + (l / 2)) 
        self.down = y + l # y-координата низа линзы
        self.F = self.center[0] + F
        canvas.create_line(x, self.up, x, self.down) # создание линзы
        #Label(canvas, text=number).place(x= x, y= y-10)
        # ----- оформление линзы ------ 
        canvas.create_line((x - 10, self.up + 10), (x, self.up), (x + 10, self.up + 10))
        canvas.create_line((x - 10, self.down - 10), (x, self.down), (x + 10, self.down - 10))

    def get_intersection(self, y= None, line= None) -> tuple:
        '''Находит точку пересечения лазера с линзой
        Если передан аргуемент y (Наколько выше центра падает лазер), то считает по нему
        Если передан аргумент line (ур-е прямой), то находит точку пересечения с помощьею него '''
        if y:
            return (self.center[0], self.center[1]-y)
        if line:
            return (self.center[0], line[0] * self.center[0] + line[1])

    def refraction_lazer(self, line, point) -> tuple:
        '''Взовращает ур-е приломленной прямой''' 
        side_axis = solution_of_the_equation(line[0], self.center) # побочная оптическая ось
        f1 = side_axis[0] * self.F + side_axis[1] # f1 = k*F + b, проекция на ось y побочного фокуса
        k = (point[1] - f1)/(point[0] - self.F) # k = (ya - yf)/(xa - xf)
        line = solution_of_the_equation(k, point)
        return (line[0], line[1], (self.F, f1))


class MyApp(Tk):

    def __init__(self):
        super().__init__()
        self.scroll_x = Scrollbar(self, orient=HORIZONTAL)
        self.canvas = Construction(self, xscrollcommand=self.scroll_x.set)
        self.scroll_x.config(command=self.canvas.xview)
        self.canvas.initUI()
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame,
                                  anchor=N + W)

        self.scroll_x.grid(row=0, column=0, sticky="we")
        self.canvas.grid(row=1, column=0, sticky="nswe")
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(1000, 400)
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
    
    def resize(self, event):
        region = self.canvas.bbox(ALL)
        self.canvas.configure(scrollregion=region)


class Construction(Canvas):
 
    def initUI(self):
        lenses = []
        pad_x, y, a, n, f, l = data_input()
        pad_y = 10
        for j in range(n):
            lenses.append(Lens(self, pad_x, pad_y, f, j+1))
            pad_x += l

        for i in range(n):
            if i == 0:
                pointA = lenses[0].get_intersection(y)                
                old_lazer = solution_of_the_equation(-tan(radians(a)), pointA) # (k, b) for y = kx + b
                self.create_line((0, old_lazer[1]), pointA, fill='red') # рисовка запускаемого лазера
            new_lazer = lenses[i].refraction_lazer(old_lazer, pointA)
            # если в скамье есть еще линзы, то рисуем лазер до нее, иначе до фокуса линзы
            if i + 1 <= n-1:
                pointB = lenses[i+1].get_intersection(line=new_lazer)
                # если лазер попадает в линзу
                if lenses[i+1].up <= pointB[1] <= lenses[i+1].down: 
                    self.create_line(pointA, pointB, fill='red')
                    pointA, pointB = pointB, (0,0)
                    old_lazer = new_lazer
                else:
                    self.create_line(pointA, pointB, fill='red')
                    break
        else:
            self.create_line(pointA, new_lazer[2], fill='red')

        self.create_line((0, lenses[-1].center[1]), (lenses[-1].F, lenses[-1].center[1]), dash= (10, 5))
 
 
def data_input():
    d = float(input("d в мм: ")) * 5
    y = float(input("y в мм: ")) * 5
    if input('Задать а? (y/N)') in ('y', 'Y'):
        a = float(input("a в градусах: ")) 
    else:
        # a = float(str(atan(y / d) * 180 / pi)[1:-4])
        a = atan(y / d) * 180 / pi
        print("ЗАДАННО a=", a)
    n = int(input("N: "))
    f = int(input("F в мм: ")) * 5
    l = float(input("L в мм: ")) * 5
    return d, y, a, n, f, l


def main():
    root = MyApp()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()