import time

minx = -21
miny = -21
maxx = 19
maxy = 19

print("%c[2J" % (27,), end="")
with open("input15.txt") as fp:
    prog = {i: int(x) for i, x in enumerate(fp.readline().split(","))}

pc = 0
rb = 0
inp = [2]
x = 0
y = 0
path = []
keymap = {"w": 1, "a": 3, "s": 2, "d": 4}
map = {(x, y): "D"}

while True:
    (flags, cmd), args = divmod(prog[pc], 100), []
    for (i, iswrite) in enumerate(
        [[], [0, 0, 1], [0, 0, 1], [1], [0], [0, 0], [0, 0], [0, 0, 1], [0, 0, 1], [0]][
            cmd % 99
        ]
    ):
        args += [prog[pc + i + 1]]
        if flags % 10 == 2:
            args[-1] += rb
        if flags % 10 != 1 and iswrite == 0:
            args[-1] = prog.get(args[-1], 0)
        flags //= 10
    orig_pc = pc
    if cmd == 1:
        prog[args[2]] = args[0] + args[1]  # add
    elif cmd == 2:
        prog[args[2]] = args[0] * args[1]  # multiply
    elif cmd == 3:
        deadend = True
        for (i, (dx, dy)) in enumerate(((0, -1), (0, 1), (-1, 0), (1, 0))):
            if (x + dx, y + dy) not in map:
                deadend = False
                break
        if deadend:
            if len(path) == 0:
                # nowhere to backtrack
                map[(0, 0)] = "."
                break
            dire = (0, 2, 1, 4, 3)[path.pop()]
            backtracking = True
        else:
            backtracking = False
            dire = i + 1
        prog[args[0]] = dire  # input
    elif cmd == 4:  # output
        outp = args[0]
        x2 = x
        y2 = y
        if dire == 1:
            y2 = y - 1
        elif dire == 2:
            y2 = y + 1
        elif dire == 3:
            x2 = x - 1
        elif dire == 4:
            x2 = x + 1
        if outp == 0:
            map[(x2, y2)] = "#"
            print(
                "%c[42m%c[%s;%sH " % (27, 27, y2 - miny + 1, x2 - minx + 1),
                end="",
                flush=True,
            )
        else:
            if not backtracking:
                path += [dire]
            if map[(x, y)] != "O":
                map[(x, y)] = "."
                print(
                    "%c[41m%c[%s;%sH " % (27, 27, y - miny + 1, x - minx + 1),
                    end="",
                    flush=True,
                )
            x = x2
            y = y2
            if outp == 1:
                map[(x, y)] = "D"
                print(
                    "%c[45m%c[%s;%sH " % (27, 27, y - miny + 1, x - minx + 1),
                    end="",
                    flush=True,
                )
            else:
                map[(x, y)] = "O"
                print(
                    "%c[44m%c[%s;%sH " % (27, 27, y - miny + 1, x - minx + 1),
                    end="",
                    flush=True,
                )
                res1 = len(path)
        time.sleep(0.01)
    elif cmd == 5 and args[0] != 0:
        pc = args[1]  # branch if true
    elif cmd == 6 and args[0] == 0:
        pc = args[1]  # branch if false
    elif cmd == 7:
        prog[args[2]] = int(args[0] < args[1])  # test less than
    elif cmd == 8:
        prog[args[2]] = int(args[0] == args[1])  # test equal
    elif cmd == 9:
        rb += args[0]  # adjust relative base
    elif cmd == 99:
        break  # halt
    if pc == orig_pc:
        # only go to the next instruction if we didn't jump
        pc += len(args) + 1

# maxx = max([k[0] for k in map.keys()])
# maxy = max([k[1] for k in map.keys()])
# minx = min([k[0] for k in map.keys()])
# miny = min([k[1] for k in map.keys()])
res2 = -1
done = False
while not done:
    prevmap = dict(map)
    done = True
    print("%c[44m" % 27)
    for y2 in range(miny, maxy + 1):
        for x2 in range(minx, maxx + 1):
            if map.get((x2, y2), " ") == ".":
                for (dx, dy) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    if prevmap[(x2 + dx, y2 + dy)] == "O":
                        done = False
                        map[(x2, y2)] = "O"
                        print(
                            "%c[%s;%sH " % (27, y2 - miny + 1, x2 - minx + 1),
                            end="",
                            flush=True,
                        )
                        break
    time.sleep(0.01)
    res2 += 1

print("%c[%s;1H%c[40m" % (27, maxy - miny + 2, 27), end="")
print("res1 = {}".format(res1))
print("res2 = {}".format(res2))
