from curtsies import Input
import time
import os


class Mapa:

    level = ""
    ancho = 0
    alto = 0
    paredes = ["#"]
    mapa = []

    def __init__(self, archivo):
        self.level = archivo
        count = 0
        with open(self.level, "r") as f:
            for i in f:
                if count > 3:
                    self.ancho = len(i.strip())
                    count += 1
                else:
                    self.mapa.append([j for j in i.strip("\n")])
            for i in self.mapa:
                while len(i) < self.ancho:
                    i.append(" ")
            self.alto = len(self.mapa)

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
        if mapa[y][x] == " ":
            x1, y2 = self.posicion
            mapa[y2][x1] = " "
            self.posicion = (x, y)
            mapa[y][x] = "Q"


def clear_console():
    if os.name == "nt":  # windows:
        os.system("cls")
    else:
        os.system("clear")


area = Mapa("level2.txt")
jugador = Player(100, 5)

x, y = 1, 1
colisiones = True

clear_console()
jugador.mover(area.mapa, x, y)
area.mostrar()
print("Oprime cualquier boton: ")

with Input(keynames='curses') as input_generator:
    # CADA VES QUE TOQUE UN TECLADO SE VA A EJECUTAR EL CODIGO DE ABAJO
    for e in input_generator:
        if e == "KEY_UP":
            if y != 0:
                y -= 1
        elif e == "KEY_DOWN":
            if y != area.alto-1:
                y += 1
        elif e == "KEY_LEFT":
            if x != 0:
                x -= 1
        elif e == "KEY_RIGHT":
            if x != area.ancho-1:
                x += 1
        elif e == "\n":
            if colisiones:
                colisiones = False
            else:
                colisiones = True
            e = "ENTER"
        elif e == " ":
            e = "SPACE"

        elif e == 'c':
            break

        if colisiones:
            if area.mapa[y][x] not in area.paredes:
                jugador.mover(area.mapa, x, y)
            else:
                x, y = jugador.posicion
        else:
            jugador.mover(area.mapa, x, y)
        clear_console()
        area.mostrar()
        print("x:", x, "y:", y)
        print("Teclado:", e)
        print("Ancho: ", area.ancho)
        print("Alto: ", area.alto)
        print(area.mapa)
