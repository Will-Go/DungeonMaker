mapa = []

with open("level.txt", "r") as f:
    leer = False
    tmp = f.readlines()
    for i in tmp:
        if leer:
            mapa.append([j for j in i.strip("\n")])
        if i.strip() == 'map':
            leer = True


print(mapa)
