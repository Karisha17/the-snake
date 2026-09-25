from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Направление движения змейки по умолчанию:
DEFAULT_DIRECTION = RIGHT

# Цвет по умолчанию для базового игрового объекта:
DEFAULT_COLOR = (255, 255, 255)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=DEFAULT_COLOR,
                 border_color=BORDER_COLOR):
        """Инициализирует атрибуты класса.

        Аргументы:
            body_color: Цвет объекта.
            border_color: Цвет границы ячейки.
        """
        self.position = (HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)
        self.body_color = body_color
        self.border_color = border_color

    def draw_cell(self, position, body_color):
        """Отрисовывает одну ячейку на игровом поле.

        Аргументы:
            position: Координаты верхнего левого угла ячейки.
            body_color: Цвет заливки ячейки.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def draw(self):
        """Отрисовка объекта класса.

        Переопределяется в дочерних классах.
        """
        raise NotImplementedError(
            'Метод draw() должен быть переопределён в дочернем классе.'
        )


class Apple(GameObject):
    """Класс Яблоко, которое съедает змейка.

    Дочерний класс класса GameObject.
    """

    def __init__(self, body_color=APPLE_COLOR, border_color=BORDER_COLOR,
                 occupied_positions=((HALF_SCREEN_WIDTH,
                                      HALF_SCREEN_HEIGHT),)):
        """Инициализирует атрибуты класса.

        Аргументы:
            body_color: Цвет объекта.
            border_color: Цвет границы ячейки.
            occupied_positions: Координаты, которые нельзя занимать.
                По умолчанию — кортеж с центром экрана.
        """
        super().__init__(body_color, border_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Задаёт случайную свободную позицию объекта.

        Аргументы:
            occupied_positions: Последовательность занятых координат,
                которые нужно исключить при выборе новой позиции.
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occupied_positions:
                self.position = new_position
                return

    def draw(self):
        """Отрисовка объекта."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка, которой управляет игрок.

    Дочерний класс класса GameObject.
    """

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        """Инициализирует атрибуты класса.

        Аргументы:
            body_color: Цвет объекта.
            border_color: Цвет границы ячейки.
        """
        super().__init__(body_color, border_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = DEFAULT_DIRECTION
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении.

        Добавляет новую голову и удаляет хвост, если длина превышает
        заданную.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def update_direction(self):
        """Обновляет направление движения змейки, если оно задано."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает события клавиатуры.

    Закрывает игру при выходе и меняет направление змейки по стрелкам.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif (event.key == pg.K_DOWN
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pg.K_LEFT
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pg.K_RIGHT
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
