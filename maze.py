import pygame
from random import randint
from typing import Sequence

from enums import Color, MoveDirection, SwitchMoveDirection
from hero import Hero, Player, Enemy, Wall
from setup import (
    DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, DEFAUL_SCREEN_FPS,
    DEFAULT_ENEMY_LIVES, DEFAULT_PLAYER_LIVES,
    DEFAULT_OBJ_SIZE,
)


class Game():
    running: bool = False
    surface: pygame.Surface
    clock: pygame.time.Clock
    fps: int
    players: Sequence[Hero]
    grid: list[list[tuple[int, int]]]

    def __init__(self,
                 width: int = DEFAULT_SCREEN_WIDTH,
                 height: int = DEFAULT_SCREEN_HEIGHT,
                 fps: int = DEFAUL_SCREEN_FPS,
                 players: Sequence[Hero] = [],
                 ) -> None:
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.players = players
        self.create_grid()
        self.add_players_to_screen()

    def create_grid(self) -> None:
        self.grid = []
        cell_count_x = self.surface.get_width() // DEFAULT_OBJ_SIZE
        cell_count_y = self.surface.get_height() // DEFAULT_OBJ_SIZE
        for row_num in range(1, cell_count_y):
            row = []
            for col_num in range(1, cell_count_x):
                row.append((
                    col_num * DEFAULT_OBJ_SIZE - DEFAULT_OBJ_SIZE // 2,
                    row_num * DEFAULT_OBJ_SIZE - DEFAULT_OBJ_SIZE // 2))
            self.grid.append(row)

    def get_cell(self, random: bool = True) -> tuple[int, int]:
        if random:
            row_num = randint(0, len(self.grid)-1)
            row = self.grid[row_num]
            col_num = randint(0, len(row)-1)
        else:
            row_num = len(self.grid) // 2
            row = self.grid[row_num]
            col_num = len(row) // 2
        cell = self.grid[row_num][col_num]
        self.grid[row_num].pop(col_num)
        if not self.grid[row_num]:
            self.grid.pop(row_num)
        return cell

    def add_players_to_screen(self) -> None:
        for hero in self.players:
            hero.surface = self.surface  # hero draws himself on shared screen
            match hero:
                case Player():  # User (Player) spawn on screen center
                    hero.lives = DEFAULT_PLAYER_LIVES
                    hero.center = self.get_cell(random=False)
                case Enemy() | Wall():  # Enemy or Wall spawn on random place
                    hero.lives = DEFAULT_ENEMY_LIVES
                    hero.center = self.get_cell(random=True)

    def get_player_instance(self) -> None | Hero:
        player = [hero for hero in self.players if hero.__class__ == Player]
        if not player:
            return None
        return player[0]

    def keydown_handler(self, key: int) -> None:
        player = self.get_player_instance()
        if not player:
            return None
        match key:
            case pygame.K_UP:
                player.direction = MoveDirection.UP
            case pygame.K_DOWN:
                player.direction = MoveDirection.DOWN
            case pygame.K_LEFT:
                player.direction = MoveDirection.LEFT
            case pygame.K_RIGHT:
                player.direction = MoveDirection.RIGHT

    def process_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    self.keydown_handler(event.key)

    def render_screen(self) -> None:
        self.surface.fill(Color.GRAY.value)
        for hero in self.players:
            hero.draw()
        pygame.display.flip()

    def get_collision_with_another_objects(self, hero: Hero) -> list[int]:
        another_player_rects = [
            player.rect for player in self.players if all([player != hero])]
        collision = hero.rect.collidelistall(another_player_rects)
        return collision

    def get_collision_with_another_player(self, hero: Hero) -> list[int]:
        another_player_rects = [
            player.rect for player in self.players if all([
                player != hero, player.__class__ != Wall])]
        collision = hero.rect.collidelistall(another_player_rects)
        return collision

    def get_collision_with_wall(self, hero: Hero) -> list[int]:
        another_player_rects = [
            player.rect for player in self.players if all([
                player != hero, player.__class__ == Wall])]
        collision = hero.rect.collidelistall(another_player_rects)
        return collision

    def step(self) -> None:
        self.players = [hero for hero in self.players if hero.lives > 0]
        if not self.get_player_instance():
            self.running = False
        for hero in self.players:
            hero.move()
            collision_with_players = self.get_collision_with_another_player(
                hero)
            collision_with_wall = self.get_collision_with_wall(hero)
            if any([collision_with_players, collision_with_wall]):
                hero.move(switch_direction=SwitchMoveDirection.BACK)
            if collision_with_players:
                hero.reduce_live()

    def run(self) -> None:
        print('GAME START')
        pygame.init()
        self.running = True
        while self.running:
            self.process_events()
            self.render_screen()
            self.step()
            self.clock.tick(self.fps) / 1000
        pygame.quit()
        print('GAME OVER')
