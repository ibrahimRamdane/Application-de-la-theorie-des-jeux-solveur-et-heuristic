# TP CSP partie cote d'azur d'Ibrahim RAMDANE
# avec mis à jour de la grille
#j'ai laissé les fichier grille1,grille2 et grille 3 dans le fichier compressé pour que vous puissiez testé 
#le bon fonctionnement du programme sur ces fichiers

from constraint import *

# -*- coding: utf-8 -*-


def readfile(filename):
    """lit une grille fournie par les profs et retourne
        les contraintes verticales, les contraintes horizontales et la grille"""
    with open(filename) as textfile:
        vertical = list(map(int, textfile.readline().split()))
        horizontal = list(map(int, textfile.readline().split()))
        grid = []
        for i in range(len(vertical)):
            line = []
            for j in range(len(horizontal)):
                line.append(0)
            grid.append(line)

        for line in textfile.readlines():
            coord = line.split()
            grid[int(coord[0])][int(coord[1])] = 1
        return vertical, horizontal, grid


def printgrid(vertical, horizontal, grid):
    """Affiche la grille correctement"""

    def prettycell(number):
        if number == 0:
            return " "
        elif number == 1:
            return "X"
        elif number == 2:
            return "F"

    def prettyline(line):
        return " ".join(map(prettycell, line))

    print("  %s" % (" ".join(map(str, vertical))))
    for line in range(len(horizontal)):
        print("%s %s" % (horizontal[line], prettyline(grid[line])))


vertical, horizontal, grid = readfile(r"grille1.txt")
printgrid(vertical, horizontal, grid)


def parasol(grid):
    # renvoie sous forme de liste les differents couples donnant la position des parasols
    L = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                L.append([i, j])
    return L


def voisin(x, grid):
    # pour chaque type de position, renvoie la liste des voisins d'une case
    if len(grid[0])-1 > x[0] > 0 and len(grid)-1 > x[1] > 0:
        return [grid[x[0]-1][x[1]], grid[x[0]-1][x[1]-1], grid[x[0]][x[1]-1], grid[x[0]+1][x[1]-1], grid[x[0]+1][x[1]], grid[x[0]+1][x[1]+1], grid[x[0]][x[1]+1], grid[x[0]-1][x[1]+1]]
    elif x[0] == 0 and len(grid)-1 > x[1] > 0:
        return [grid[x[0]][x[1]-1], grid[x[0]+1][x[1]-1], grid[x[0]+1][x[1]], grid[x[0]+1][x[1]+1], grid[x[0]][x[1]+1]]
    elif x[0] == 0 and x[1] == 0:
        return [grid[x[0]+1][x[1]], grid[x[0]+1][x[1]+1], grid[x[0]][x[1]+1]]
    elif x[0] == 0 and x[1] == len(grid)-1:
        return [grid[x[0]][x[1]-1], grid[x[0]+1][x[1]-1], grid[x[0]+1][x[1]]]
    elif x[0] == len(grid[0])-1 and x[1] == len(grid)-1:
        return [grid[x[0]-1][x[1]], grid[x[0]-1][x[1]-1], grid[x[0]][x[1]-1]]
    elif x[0] == len(grid[0])-1 and x[1] == 0:
        return [grid[x[0]-1][x[1]], grid[x[0]][x[1]+1], grid[x[0]-1][x[1]+1]]
    elif len(grid[0])-1 > x[0] > 0 and x[1] == 0:
        return [grid[x[0]-1][x[1]], grid[x[0]+1][x[1]], grid[x[0]+1][x[1]+1], grid[x[0]][x[1]+1], grid[x[0]-1][x[1]+1]]
    elif len(grid[0])-1 > x[0] > 0 and x[1] == len(grid)-1:
        return [grid[x[0]-1][x[1]], grid[x[0]-1][x[1]-1], grid[x[0]][x[1]-1], grid[x[0]+1][x[1]-1], grid[x[0]+1][x[1]]]
    elif x[0] == len(grid[0])-1 and len(grid)-1 > x[1] > 0:
        return [grid[x[0]-1][x[1]], grid[x[0]-1][x[1]-1], grid[x[0]][x[1]-1],  grid[x[0]][x[1]+1], grid[x[0]-1][x[1]+1]]


def voisin_et_centre(x, grid):
    # rajoute la position de la case pour laquel on recherche les voisin
    return [grid[x[0]][x[1]]] + voisin(x, grid)


def voisin_sans_diag_et_centre(x, grid):
    # renvoie la liste des voisins direct diagonale exclu et la case dont on recherche les voisins
    if len(grid[0])-1 > x[0] > 0 and len(grid)-1 > x[1] > 0:
        return [grid[x[0]][x[1]]] + [grid[x[0]-1][x[1]],  grid[x[0]][x[1]-1],  grid[x[0]+1][x[1]], grid[x[0]][x[1]+1]]
    elif x[0] == 0 and len(grid)-1 > x[1] > 0:
        return [grid[x[0]][x[1]]] + [grid[x[0]][x[1]-1],  grid[x[0]+1][x[1]],  grid[x[0]][x[1]+1]]
    elif x[0] == 0 and x[1] == 0:
        return [grid[x[0]][x[1]]] + [grid[x[0]+1][x[1]],  grid[x[0]][x[1]+1]]
    elif x[0] == 0 and x[1] == len(grid)-1:
        return [grid[x[0]][x[1]]] + [grid[x[0]][x[1]-1], grid[x[0]+1][x[1]]]
    elif x[0] == len(grid[0])-1 and x[1] == len(grid)-1:
        return [grid[x[0]][x[1]]] + [grid[x[0]-1][x[1]], grid[x[0]][x[1]-1]]
    elif x[0] == len(grid[0])-1 and x[1] == 0:
        return [grid[x[0]][x[1]]] + [grid[x[0]-1][x[1]], grid[x[0]][x[1]+1]]
    elif len(grid[0])-1 > x[0] > 0 and x[1] == 0:
        return [grid[x[0]][x[1]]] + [grid[x[0]-1][x[1]], grid[x[0]+1][x[1]], grid[x[0]][x[1]+1]]
    elif len(grid[0])-1 > x[0] > 0 and x[1] == len(grid)-1:
        return [grid[x[0]][x[1]]] + [grid[x[0]-1][x[1]], grid[x[0]][x[1]-1], grid[x[0]+1][x[1]]]
    elif x[0] == len(grid[0])-1 and len(grid)-1 > x[1] > 0:
        return [grid[x[0]][x[1]]] + [grid[x[0]-1][x[1]], grid[x[0]][x[1]-1],  grid[x[0]][x[1]+1]]


def famille_parasol(*n):
    if 1 in n[1:] and n[0] == 2:
        # test si il ya au moisune famille dans le voisinnage d'un parassol (diagonal exclu)
        return True
    elif n[0] == 0:
        # si la cas n'est ni une famille ni un parassol pas de contrainte sur les familles au voisinnage
        return True


def une_seul_famille(*n):
    if 2 not in n[1:] and n[0] == 2:
        # test si une famille n'a pas de famille dans son voisinage
        return True
    elif n[0] == 0:
        # si la cas n'est pas une famille pas de contrainte sur les familles dans le voisinnage
        return True


def lig_col(grid):
    # renvoie une premiere liste de la somme des variables de chaque ligne et une seconde liste de la somme
    # des variables de chaque colonne
    L = []
    for i in range(len(grid)):
        l = 0
        for j in range(len(grid[0])):
            l = l+grid[i][j]
        L.append(l)
    C = []
    for j in range(len(grid[0])):
        c = 0
        for i in range(len(grid)):
            c = c+grid[i][j]
        C.append(c)
    return L, C


def solveur(grid):
    problem = Problem()
    # création des variable pour chaque case
    Q = [["Q%i%i" % (i+1, j+1) for j in range(len(grid))]
         for i in range(len(grid[0]))]
    i = 0

    for row in Q:
        problem.addVariables(row, [0, 1, 2])
        # contraint le nombre de famille pour chaque ligne corespondant à celui imposé par les regles
        problem.addConstraint(ExactSumConstraint(
            horizontal[i]*2+lig_col(grid)[0][i]), row)
        i = i+1
    for j in range(len(Q[0])):
        # contraint le nombre de famille pour chaque ligne corespondant à celui imposé par les regles
        problem.addConstraint(ExactSumConstraint(vertical[j]*2+lig_col(grid)[1][j]), [
                              Q[i][j] for i in range(len(Q))])

    # on conserve la position des parassols par rapport à celle imposé par la grille
    for i in range(8):
        for j in range(8):
            if grid[i][j] != 0:
                def c(variable_value, value_in_table=grid[i][j]):
                    if variable_value == value_in_table:
                        return True

                problem.addConstraint(c, ["Q%i%i" % (i+1, j+1)])

    for i in range(len(Q)):
        for j in range(len(Q)):
            if [i, j] not in parasol(grid):
                # on contraint la position des familled de tel sorte qu'une famille n'est aucune famille dans son voisinnage
                problem.addConstraint(
                    une_seul_famille, voisin_et_centre([i, j], Q))
                # on contraint la position des familles de tel sorte que chaque parason ait dans son voisinnage au moins une famille diagonale exclu
                problem.addConstraint(
                    famille_parasol, voisin_sans_diag_et_centre([i, j], Q))

    sol = problem.getSolutions()
    # on réarrenge la solution sous forme liste pour ensuite pouvoir mettre à jour la grille avec le resultat final
    for k in range(len(sol)):
        L = [[sol[k]["Q%i%i" % (i+1, j+1)] for j in range(len(Q))]
             for i in range(len(Q))]
        printgrid(vertical, horizontal, L)


solveur(readfile("grille1.txt")[2])
