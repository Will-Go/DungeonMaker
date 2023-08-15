# from curtsies import Input
import time
import os
import keyboard as kb


class Mapa:

    level = ""
    ancho = 0
    alto = 0
    paredes = []
    mapa = []

    def __init__(self, archivo):
        self.level = archivo
        leer = False
        with open(self.level, "r") as f:
            tmp = f.readlines()
            self.ancho = int(tmp[0].strip())
            self.paredes.extend(tmp[1].strip().split())
            for i in tmp:
                if leer:
                    self.mapa.append([j for j in i.strip("\n")])
                if i.strip() == 'map':
                    leer = True

        for i in self.mapa:
            while len(i) < self.ancho:
                i.append(" ")
        self.alto = len(self.mapa)
        del tmp

    def mostrar(self):
        print("\t\t"+"="*(self.ancho+2))
        for i in self.mapa:
            print("\t\t|", end="")
            for j in i:
                print(j, end="")
            print("|")
        print("\t\t"+"="*(self.ancho+2))


class Player:
    vida = 0
    ataque = 0
    inventario = []
    posicion = ()

    def __init__(self, vida, ataque, inventario=[], posicion=(1, 1)):
        self.vida = vida
        self.ataque = ataque
        self.inventario = inventario
        self.posicion = posicion

    def mover(self, mapa, x, y):
        if mapa[y][x] not in area.paredes:
            x1, y2 = self.posicion
            mapa[y2][x1] = " "
            self.posicion = (x, y)
            mapa[y][x] = "Q"
        else:
            x1, y2 = self.posicion
            mapa[y2][x1] = " "

    def ataque(self, mapa):
        pass


class Enemy:
    lista = []

    def __init__(self):
        pass


def clear_console():
    if os.name == "nt":  # windows:
        os.system("cls")
    else:
        os.system("clear")

# Control de Teclados


def key_press(key):
    global colisiones, x, y, area, jugador, parar
    if key.name == "up":
        if y != 0:
            y -= 1

    elif key.name == "down":
        if y != area.alto-1:
            y += 1

    elif key.name == "left":
        if x != 0:
            x -= 1

    elif key.name == "right":
        if x != area.ancho-1:
            x += 1

    elif key.name == "enter":
        if colisiones:
            colisiones = False
            key.name = "colision OFF"
        else:
            colisiones = True
            key.name = "colision ON"
    elif key.name == "esc":
        raise KeyboardInterrupt

    if colisiones:
        if area.mapa[y][x] not in area.paredes:
            jugador.mover(area.mapa, x, y)
        else:
            x, y = jugador.posicion
    else:
        jugador.mover(area.mapa, x, y)

    clear_console()
    print(banner)
    area.mostrar()
    print("x:", x, "y:", y)
    print("Teclado:", key.name)


banner = """
██╗  ██╗███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗
██║ ██╔╝████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝
█████╔╝ ██╔██╗ ██║██║██║  ███╗███████║   ██║   
██╔═██╗ ██║╚██╗██║██║██║   ██║██╔══██║   ██║   
██║  ██╗██║ ╚████║██║╚██████╔╝██║  ██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
"""


area = Mapa("level.txt")
jugador = Player(100, 5)

x, y = 0, 0
colisiones = True
parar = False
jugador.mover(area.mapa, x, y)

clear_console()
print(area.mapa)
print(area.paredes)
print(area.alto)
print(area.ancho)
print(banner)
area.mostrar()
print("Oprime cualquier boton: ")

kb.on_press(key_press)
try:
    kb.wait()
except KeyboardInterrupt:
    print("Adios")

# TODO Enimies and attack

# Hola muy buenas a todos
