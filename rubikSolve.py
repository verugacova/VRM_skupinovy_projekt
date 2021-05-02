from rubik.cube import Cube
from rubik.solve import Solver
import random
from rubik_solver import utils
import socket

HOST = '127.0.0.1'
PORT = 31254

c = Cube("OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR")

def rozloz_kostku(c, n=20):

    moves = [c.F, c.R, c.U, c.L, c.B, c.D, c.Fi, c.Ri, c.Ui, c.Li, c.Bi, c.Di]

    for _ in range(n):
        random.choice(moves)()
    return c

def uprav_kostku(c):

    c = rozloz_kostku(c)
    c = c._color_list()
    c = str(''.join(c))
    c = c.lower()

    sideA = c[0:9]
    sideB = c[9:12] + c[21:24] + c[33:36]
    sideC = c[12:15] + c[24:27] + c[36:39]
    sideD = c[15:18] + c[27:30] + c[39:42]
    sideE = c[18:21] + c[30:33] + c[42:45]
    sideF = c[45:55]

    c = sideA + sideB + sideC + sideD + sideE + sideF

    return c

def replace(c, a, b):

    c = c.replace(a, "i")
    c = c.replace(b, a)
    c = c.replace("i", b)

    return c

def sloz_kostku(c, level = 2):

    if level == 1:
        le = utils.solve(c, 'Beginner')
        print("level 1: \n", le)
        leM = uprav_moves(le)
    elif level == 2:
        le = utils.solve(c, 'CFOP')
        print("level 2: \n", le)
        leM = uprav_moves(le)
    elif level == 3:
        le = utils.solve(c, 'Kociemba')
        print("level 3: \n", le)
        leM = uprav_moves(le)
    return leM

c = uprav_kostku(c)
c = str(replace(c, "o", "y"))
c = str(replace(c, "o", "b"))
c = str(replace(c, "w", "r"))

def uprav_moves(moves):
    
    moves = ''.join(map(str, moves))
    m = ["R", "L", "U", "B", "D", "F", "Y", "M", "S", "E", "X", "Z"]
    for i in range(len(m)):
        moves = moves.replace(m[i]+"'", m[i]+m[i]+m[i])
        moves = moves.replace(m[i]+"2", m[i]+m[i])
    print("\nUpraveno: \n", moves, "\n", 200*"-")
    return moves

def send_to_server(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())
        data = s.recv(1024)
        return data

level1 = sloz_kostku(c, 1)
level2 = sloz_kostku(c, 2)
level3 = sloz_kostku(c, 3)

print("OUTPUT: ", level3)

send_to_server(level3)


