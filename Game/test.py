import astar_lib


game_map = [
    "111111",
    "100101",
    "110001",
    "111111"
]

py, px = 1, 1
by, bx = 2, 4


print(astar_lib.astar(game_map, py, px, by, bx))
