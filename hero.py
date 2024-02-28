import pygame
from random import choice

from enums import Color, MoveDirection, SwitchMoveDirection
from setup import DEFAULT_OBJ_SIZE, DEFAULT_SPEED
from text import Text


class Hero():
    color: Color = Color.BLACK
    size: int = DEFAULT_OBJ_SIZE
    speed: int = DEFAULT_SPEED
    center: tuple[int, int] = (0, 0)
    direction: MoveDirection = MoveDirection.UP
    surface: pygame.surface.Surface
    rect: pygame.Rect
    lives: int = 0

    def reduce_live(self) -> None:
        self.lives -= 1

    def draw_lives(self) -> None:
        Text(str(self.lives), self.rect.center, 20, Color.BLACK.value
             ).draw(self.surface)

    def draw(self, draw_lives: bool = True) -> None:
        left = self.center[0] - self.size // 2
        top = self.center[1] - self.size // 2
        self.rect = pygame.draw.rect(
            self.surface, self.color.value, pygame.Rect(
                left, top, self.size, self.size,
            )
        )
        if draw_lives:
            self.draw_lives()

    def get_rangom_direction(
            self, exclude: list[MoveDirection] = []) -> MoveDirection:
        direction_list = list(MoveDirection)
        if exclude:
            for direction in exclude:
                direction_list.remove(direction)
        return choice(direction_list)

    def resolve_collision_with_screen_border(self) -> None:
        half_size = self.size // 2
        center_x = self.center[0]
        center_y = self.center[1]
        screen_width = self.surface.get_width()
        screen_height = self.surface.get_height()

        if center_x - half_size < 0:
            self.direction = self.get_rangom_direction()
        elif center_x + half_size > screen_width:
            self.direction = self.get_rangom_direction()

        if center_y - half_size < 0:
            self.direction = self.get_rangom_direction()
        elif center_y + half_size > screen_height:
            self.direction = self.get_rangom_direction()

    def collision_handler(self) -> None:
        self.resolve_collision_with_screen_border()

    def move(
            self,
            switch_direction: SwitchMoveDirection = SwitchMoveDirection.NO
            ) -> None:
        match switch_direction:
            case SwitchMoveDirection.BACK:
                BACK_DIRECTION_MAPPER = {
                    MoveDirection.UP: MoveDirection.DOWN,
                    MoveDirection.DOWN: MoveDirection.UP,
                    MoveDirection.LEFT: MoveDirection.RIGHT,
                    MoveDirection.RIGHT: MoveDirection.LEFT,
                }
                self.direction = BACK_DIRECTION_MAPPER[self.direction]
            case SwitchMoveDirection.RANDOM:
                self.direction = self.get_rangom_direction(
                    exclude=[self.direction])

        self.rect = self.rect.move(
            self.direction.value[0] * self.speed,
            self.direction.value[1] * self.speed,
            )
        self.center = self.rect.center
        self.collision_handler()


class Player(Hero):
    def __init__(self) -> None:
        super().__init__()
        self.color = Color.YELLOW

    def draw(self, draw_lives: bool = True) -> None:
        self.rect = pygame.draw.circle(
                self.surface, self.color.value, self.center, self.size // 2
            )
        if draw_lives:
            self.draw_lives()


class Enemy(Hero):
    def __init__(self) -> None:
        super().__init__()
        self.color = choice([Color.RED, Color.BLUE, Color.GREEN])
        self.direction = choice(list(MoveDirection))


class Wall(Hero):
    def __init__(self) -> None:
        super().__init__()
        self.color = Color.WHITE
        self.speed = 0

    def draw(self, draw_lives: bool = False) -> None:
        return super().draw(draw_lives)

    def reduce_live(self) -> None:
        return None
