from maze import Game
from hero import Player, Enemy, Wall
from setup import DEFAULT_ENEMY_COUNT, DEFAULT_WALL_COUNT


def main() -> None:
    players = [
        Player(),
        *[Wall() for _ in range(DEFAULT_WALL_COUNT)],
        *[Enemy() for _ in range(DEFAULT_ENEMY_COUNT)],
        ]
    game = Game(players=players)
    game.run()


if __name__ == "__main__":
    main()
