import tkinter as tk
from tkinter import colorchooser

# Абстрактный класс, представляющий общую основу для фигур.
class Shape:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

# Класс точки, наследует базовые свойства из Shape.
class Point(Shape):
    def __init__(self, x, y, color, thickness):
        super().__init__(color, thickness) # Инициализируем базовые свойства
        self.x = x # Координата x
        self.y = y # Координата y
    # Метод для рисования точки на холсте
    def draw(self, canvas):
        radius = self.thickness // 2
        return canvas.create_oval(
            self.x - radius, self.y - radius,
            self.x + radius, self.y + radius,
            fill=self.color, outline=self.color
        )

# Класс линии, наследует Shape.
class Line(Shape):
    def __init__(self, start_point, end_point, color, thickness):
        super().__init__(color, thickness)
        self.start_point = start_point # Начальная точка
        self.end_point = end_point # Конечная точка
    # Метод для рисования линии на холсте
    def draw(self, canvas):
        return canvas.create_line(
            self.start_point.x, self.start_point.y,
            self.end_point.x, self.end_point.y,
            fill=self.color, width=self.thickness
        )

# Класс круга.
class Circle(Shape):
    def __init__(self, start_point, end_point, color, thickness):
        super().__init__(color, thickness)
        self.start_point = start_point
        self.end_point = end_point
    # Метод для рисования круга
    def draw(self, canvas):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y
        return canvas.create_oval(x1, y1, x2, y2, outline=self.color, width=self.thickness)

# Класс прямоугольника.
class Rectangle(Shape):
    def __init__(self, start_point, end_point, color, thickness):
        super().__init__(color, thickness)
        self.start_point = start_point
        self.end_point = end_point
    # Метод для рисования прямоугольника
    def draw(self, canvas):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y
        return canvas.create_rectangle(x1, y1, x2, y2, outline=self.color, width=self.thickness)

# Класс треугольника.
class Triangle(Shape):
    def __init__(self, start_point, end_point, color, thickness):
        super().__init__(color, thickness)
        self.start_point = start_point
        self.end_point = end_point
    # Метод для рисования треугольник
    def draw(self, canvas):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y

        x3 = (x1 + x2) / 2
        y3 = min(y1, y2) - abs(x2 - x1) / 2

        return canvas.create_polygon(
            x1, y1, x2, y2, x3, y3,
            outline=self.color, width=self.thickness, fill=''
        )

# Основной класс графического редактора.
class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()
        # Инициализация параметров
        self.color = "black" # Цвет по умолчанию
        self.thickness = 2 # Толщина по умолчанию
        self.start_point = None
        self.preview_id = None
        self.shapes = [] # Список нарисованных фигур
        self.free_draw_shapes = [] # Временный список для свободного рисования
        self.current_mode = "free_draw" # Режим по умолчанию

        self.create_ui() # Создаем элементы управления

    def create_ui(self):
        # Кнопки и поля
        color_button = tk.Button(self.root, text="Цвет", command=self.choose_color)
        thickness_label = tk.Label(self.root, text="Толщина:")
        self.thickness_entry = tk.Entry(self.root, width=5)
        self.thickness_entry.insert(0, "2")
        undo_button = tk.Button(self.root, text="Отмена", command=self.undo)
        clear_button = tk.Button(self.root, text="Очистить", command=self.clear_canvas)
        free_draw_button = tk.Button(self.root, text="Рисование", command=lambda: self.set_mode("free_draw"))
        circle_button = tk.Button(self.root, text="Круг", command=lambda: self.set_mode("circle"))
        rectangle_button = tk.Button(self.root, text="Прямоугольник", command=lambda: self.set_mode("rectangle"))
        triangle_button = tk.Button(self.root, text="Треугольник", command=lambda: self.set_mode("triangle"))
        line_button = tk.Button(self.root, text="Прямая линия", command=lambda: self.set_mode("line"))
        point_button = tk.Button(self.root, text="Точка", command=lambda: self.set_mode("point"))
        
        # Размещение элементов
        color_button.pack(side=tk.LEFT)
        thickness_label.pack(side=tk.LEFT)
        self.thickness_entry.pack(side=tk.LEFT)
        undo_button.pack(side=tk.LEFT)
        clear_button.pack(side=tk.LEFT)
        free_draw_button.pack(side=tk.LEFT)
        circle_button.pack(side=tk.LEFT)
        rectangle_button.pack(side=tk.LEFT)
        triangle_button.pack(side=tk.LEFT)
        line_button.pack(side=tk.LEFT)
        point_button.pack(side=tk.LEFT)

        # Привязка событий к холсту
        self.canvas.bind("<Button-1>", self.on_mouse_down) # Нажатие кнопки мыши
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag) # Перетаскивание
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up) # Отпускание кнопки
    
    # Выбор цвета
    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    # Установка режима
    def set_mode(self, mode):
        self.current_mode = mode
        self.start_point = None
        self.free_draw_shapes.clear()
        self.root.title(f"Графический редактор - Режим: {mode.capitalize()}")

    # Обработчик нажатия мыши
    def on_mouse_down(self, event):
        self.start_point = Point(event.x, event.y, self.color, self.thickness)
        if self.current_mode == "free_draw":
            self.preview_id = self.start_point.draw(self.canvas)
            self.free_draw_shapes.append([self.preview_id, self.start_point])

        elif self.current_mode == "point":
            self.start_point.draw(self.canvas)

    # Обработчик перетаскивания
    def on_mouse_drag(self, event):
        self.thickness = int(self.thickness_entry.get())  # Обновление толщины
        if self.current_mode == "free_draw":
            point = Point(event.x, event.y, self.color, self.thickness)
            line = Line(self.start_point, point, self.color, self.thickness)
            self.start_point = point
            shape_id = line.draw(self.canvas)
            self.free_draw_shapes[-1].append(shape_id)
        elif self.current_mode == "circle" and self.start_point:
            if self.preview_id:
                self.canvas.delete(self.preview_id)  # Удаляем старый предварительный вид
            end_point = Point(event.x, event.y, self.color, self.thickness)
            shape = Circle(self.start_point, end_point, self.color, self.thickness)
            self.preview_id = shape.draw(self.canvas)
        elif self.current_mode == "rectangle" and self.start_point:
            if self.preview_id:
                self.canvas.delete(self.preview_id)
            end_point = Point(event.x, event.y, self.color, self.thickness)
            shape = Rectangle(self.start_point, end_point, self.color, self.thickness)
            self.preview_id = shape.draw(self.canvas)
        elif self.current_mode == "triangle" and self.start_point:
            if self.preview_id:
                self.canvas.delete(self.preview_id)
            end_point = Point(event.x, event.y, self.color, self.thickness)
            shape = Triangle(self.start_point, end_point, self.color, self.thickness)
            self.preview_id = shape.draw(self.canvas)
        elif self.current_mode == "line" and self.start_point:
            if self.preview_id:
                self.canvas.delete(self.preview_id)
            end_point = Point(event.x, event.y, self.color, self.thickness)
            line = Line(self.start_point, end_point, self.color, self.thickness)
            self.preview_id = line.draw(self.canvas)
    # Завершение рисования фигуры
    def on_mouse_up(self, event):
        self.thickness = int(self.thickness_entry.get()) 
        if self.current_mode in ["circle", "rectangle", "triangle", "line"] and self.start_point:
            end_point = Point(event.x, event.y, self.color, self.thickness)
            if self.current_mode == "circle":
                shape = Circle(self.start_point, end_point, self.color, self.thickness)
            elif self.current_mode == "rectangle":
                shape = Rectangle(self.start_point, end_point, self.color, self.thickness)
            elif self.current_mode == "triangle":
                shape = Triangle(self.start_point, end_point, self.color, self.thickness)
            elif self.current_mode == "line":
                shape = Line(self.start_point, end_point, self.color, self.thickness)
            shape_id = shape.draw(self.canvas)
            self.shapes.append([(shape_id, shape)])
            self.start_point = None
            if self.preview_id:
                self.canvas.delete(self.preview_id)
                self.preview_id = None
    # Отмена последнего действия
    def undo(self):
        if self.free_draw_shapes:
            for shape in self.free_draw_shapes[-1]:
                self.canvas.delete(shape)
            self.free_draw_shapes.pop()
        elif self.shapes:
            last_shape = self.shapes.pop()
            for shape_id, _ in last_shape:
                self.canvas.delete(shape_id)
     # Очистка холста
    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()
        self.free_draw_shapes.clear()


root = tk.Tk()
editor = GraphicEditor(root)
root.mainloop()