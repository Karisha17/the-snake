from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=DEFAULT_COLOR):
        """Инициализирует атрибуты класса.

        Аргументы:
            body_color: Цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта класса.

        Переопределяется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс Яблоко, которое съедает змейка.

    Дочерний класс класса GameObject.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализирует атрибуты класса.

        Аргументы:
            body_color: Цвет объекта.
        """
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задает случайную позицию объекта."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовка объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка, которой управляет игрок.

    Дочерний класс класса GameObject.
    """

    def __init__(self, direction=RIGHT, body_color=SNAKE_COLOR):
        """Инициализирует атрибуты класса.

        Аргументы:
            body_color: Цвет объекта.
            direction: Направление движения объекта.
        """
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = direction
        self.next_direction = None
        self.last = None

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
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку и затирает её последний сегмент."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змейки, если оно задано."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает события клавиатуры.

    Закрывает игру при выходе и меняет направление змейки по стрелкам.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif (event.key == pygame.K_DOWN
                    and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                    and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                    and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.move()

        for i in range(1, len(snake.positions)):
            if snake.positions[0] == snake.positions[i]:
                snake.reset()
                break

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
