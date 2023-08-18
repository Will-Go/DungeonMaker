# from curtsies import Input
import time
import os
import keyboard as kb
import colorama as color


class Mapa:

    level = ""
    ancho = 0
    alto = 0
    paredes = []
    mapa = []

    def __init__(self, archivo):
        self.level = archivo
        leer = False
        leerEnemigo = False
        with open(self.level, "r") as f:
            tmp = f.readlines()
            self.ancho = int(tmp[0].strip())
            self.paredes.extend(tmp[1].strip().split())
            playerAtr = tmp[2].strip().split()
            nuevoJugador = Player(int(playerAtr[1]), int(playerAtr[2]), playerAtr[0], posicion=(
                int(playerAtr[3]), int(playerAtr[4])))
            for i in tmp:
                # Aqui va a comenzar a buscar por la palabra "enemy", hasta que lo encuentra va a comenzar a leer los atributos de los enemigos
                if leerEnemigo:
                    if i.strip() == 'end':
                        leerEnemigo = False
                    else:
                        if i.strip() != "":
                            enemigo = i.strip().split()
                            nuevoEnemigo = Enemy(
                                enemigo[0], int(enemigo[1]), int(enemigo[2]))
                elif i.strip() == 'enemy':
                    leerEnemigo = True

                # Aqui va a comenzar a buscar por la palabra "map" hasta que lo encuentra va comenzar a construir el mapa
                if leer:
                    self.mapa.append([j for j in i.strip("\n")])
                elif i.strip() == 'map':
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
    lista = []

    simbolo = ""
    vida = 0
    ataque = 0
    inventario = []
    posicion = ()
    vivo = True

    def __init__(self, vida, ataque, simbolo="Q", inventario=[], posicion=(1, 1)):
        if vida > 0:
            self.vida = vida
        else:
            self.vivo = False
        self.ataque = ataque
        self.simbolo = simbolo
        self.inventario = inventario
        self.posicion = posicion
        Player.lista.append(self)

    def mover(self, mapa, x, y):
        if mapa[y][x] not in area.paredes:
            # DETECTA SI ESTA ENCIMA DE UN ENEMIGO
            if mapa[y][x] in Enemy.hashMap.keys():
                enemigo = Enemy.hashMap[mapa[y][x]]
                enemigoVida = enemigo.vida
                while enemigoVida > 0 and self.vida > 0:
                    enemigoVida -= self.ataque
                    self.vida -= enemigo.ataque
            if self.vida <= 0:
                self.vivo = False

            x1, y2 = self.posicion
            mapa[y2][x1] = " "
            self.posicion = (x, y)
            if self.vivo:
                mapa[y][x] = color.Fore.BLUE+self.simbolo+color.Fore.RESET
            else:
                mapa[y][x] = color.Fore.RED+"X"+color.Fore.RESET

        else:
            x1, y2 = self.posicion
            mapa[y2][x1] = " "

    def mostrar_stats(self):
        print(self.simbolo+":")
        print("\tLife:", self.vida)
        print("\tAttack:", self.ataque)


class Enemy:
    hashMap = {}
    simbol = ""
    vida = 0
    ataque = 0

    def __init__(self, simbol, vida, ataque):
        self.simbol = simbol
        self.vida = vida
        self.ataque = ataque
        Enemy.hashMap[simbol] = self


def clear_console():
    if os.name == "nt":  # windows:
        os.system("cls")
    else:
        os.system("clear")

# Control de Teclados


def key_press(key):
    global colisiones, x, y, area, jugador, banner
    if jugador.vivo:
        if key.name in ["up", "flecha arriba"]:
            if y != 0:
                y -= 1

        elif key.name in ["down", "flecha abajo"]:
            if y != area.alto-1:
                y += 1

        elif key.name in ["left", "flecha izquierda"]:
            if x != 0:
                x -= 1

        elif key.name in ["right", "flecha derecha"]:
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
    else:
        return

    if not jugador.vivo:
        banner = loseBanner
    clear_console()
    print(banner)
    area.mostrar()
    print("x:", x, "y:", y)
    jugador.mostrar_stats()
    print("Teclado:", key.name)
    if not jugador.vivo:
        print("PRESS 'esc'")


# THIS FONT IS CALL "ANSI SHADOW" FROM "http://patorjk.com/software/taag/"
loseBanner = color.Fore.RED + """
██╗   ██╗ ██████╗ ██╗   ██╗    ██╗      ██████╗ ███████╗███████╗
╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║     ██╔═══██╗██╔════╝██╔════╝
 ╚████╔╝ ██║   ██║██║   ██║    ██║     ██║   ██║███████╗█████╗  
  ╚██╔╝  ██║   ██║██║   ██║    ██║     ██║   ██║╚════██║██╔══╝  
   ██║   ╚██████╔╝╚██████╔╝    ███████╗╚██████╔╝███████║███████╗
   ╚═╝    ╚═════╝  ╚═════╝     ╚══════╝ ╚═════╝ ╚══════╝╚══════╝
""" + color.Fore.RESET

banner = color.Fore.BLUE+"""
██╗  ██╗███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗
██║ ██╔╝████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝
█████╔╝ ██╔██╗ ██║██║██║  ███╗███████║   ██║   
██╔═██╗ ██║╚██╗██║██║██║   ██║██╔══██║   ██║   
██║  ██╗██║ ╚████║██║╚██████╔╝██║  ██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
""" + color.Fore.RESET


area = Mapa("level.txt")
jugador = Player.lista[0]
x, y = jugador.posicion
jugador.mover(area.mapa, x, y)
colisiones = True


clear_console()
print(area.mapa)
print(area.paredes)
print(area.alto)
print(area.ancho)
print("Enemigos")
for i in Enemy.hashMap.values():
    print(i.simbol, ":", "\n\tLife:", i.vida, "\n\tAttack:", i.ataque)
print(banner)
area.mostrar()
print("Oprime cualquier boton: ")

try:

    kb.on_press(key_press)
    kb.wait('esc')
except KeyboardInterrupt:
    pass

print("END")

# TODO Hero, attack, weaponse, items and inventory
