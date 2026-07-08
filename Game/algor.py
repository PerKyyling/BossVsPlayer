
from collections import deque



def pathfinder(map, start, target):

    queue = deque([start])

    vs = {start}
    order = {}

    mas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:

        curr = queue.popleft()

        if curr == target:
            break

        nx = curr[0]; ny = curr[1]

        for nb_x, nb_y in mas:

            new_curr = nb_x + nx, nb_y + ny

            if new_curr not in vs and (len(map) > new_curr[1] >= 0) and (len(map[0]) > new_curr[0] >= 0):

                if map[new_curr[1]][new_curr[0]] != '1':
                    vs.add(new_curr)

                    queue.append(new_curr)
                    order[new_curr] = curr

    if target not in order and start != target:
        return []

    one = target; p = []
    while one != start:
        p.append(one)
        one = order[one]

    p.append(start)
    return p[::-1]



def to_inst(game_map, by, bx, py, px):


    p = pathfinder(game_map, (px, py), (bx, by))

    if not p: return ""

    ans = []
    mas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    mas_sl = {(1, 0): 'R', (-1, 0): 'L', (0, 1): 'D', (0, -1): 'U'}

    for i in range(len(p) - 1):
        for rev in mas:

            if (rev[0] + p[i][0], rev[1] + p[i][1]) == p[i + 1]:

                ans.append(mas_sl[rev])

    return "".join(ans)



