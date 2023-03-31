# TP CSP partie cinéma d'Ibrahim RAMDANE
# La personne qui aime les m&m’s est Nicolas


from constraint import *


# On crée les variables

prenom = ['Danielle', 'Joshua', 'Nicolas', 'Annabel']

couleur = ['noir', 'bleu', 'vert', 'rouge']

film = ['action', 'comedie', 'thriller', 'horreur']

friandise = ['chips', 'cookies', 'mms', 'popcorn']

age = ['21', '22', '23', '24']

ensemble_variable = prenom + couleur + film + friandise + age


problem = Problem()

# Pour chacune des variables(prenom,couleur,...)  on affecte une valeur 0 et 3 qui indique la position de l'eleve

problem.addVariables(ensemble_variable, range(4))


# Pour un meme groupe de variable (prenom,...) les valeirs affecté aux variables doivent etre differentes
# (car chaque variable d'un groupe de variable correspond a une et unique personne)

problem.addConstraint(AllDifferentConstraint(), prenom)
problem.addConstraint(AllDifferentConstraint(), couleur)
problem.addConstraint(AllDifferentConstraint(), film)
problem.addConstraint(AllDifferentConstraint(), friandise)
problem.addConstraint(AllDifferentConstraint(), age)


# 1. Joshua est à l’une des extrémités
def extremité(var):
    if var == 0 or var == 3:
        return True


problem.addConstraint(extremité, ['Joshua'])


# 2. L’élève portant un t-shirt noir est à gauche de l’élève le plus jeune (mais pas nécessairement juste à gauche)

def gauche(var1, var2):
    if var1 >= var2-1:
        return True


problem.addConstraint(gauche, ['noir', '21'])


# 3. Joshua aime les films d’horreur

def identique(var1, var2):
    if var1 == var2:
        return True


problem.addConstraint(identique, ['Joshua', 'horreur'])


# 4. L’élève qui a 24 ans est à la 3ème position

problem.addConstraint(ExactSumConstraint(2), ['24'])


# 5. L’élève avec le t-shirt rouge est quelque part entre l’élève de 23 ans et celui ou celle qui aime les films d’action
# (dans cet ordre)

def milieu(var1, var2, var3):
    if var2 > var1 and var2 < var3:
        return True


problem.addConstraint(milieu, ['23', 'rouge', 'action'])


# 6. Danielle aime les Thrillers

problem.addConstraint(identique, ['Danielle', 'thriller'])


# 7. L’élève qui aime les cookies est à l’une des extrémités

problem.addConstraint(extremité, ['cookies'])


# 8. L’élève portant un t-shirt noir est directement à gauche de celui qui aime les Thrillers

def gauche_dir(var1, var2):
    if var1 == var2-1:
        return True


problem.addConstraint(gauche_dir, ['noir', 'thriller'])

# 9. L’élève qui aime les m&m’s est exactement à droite de celui ou celle qui aime les comédies


def droite(var1, var2):
    if var1 == var2+1:
        return True


problem.addConstraint(droite, ['mms', 'comedie'])


# 10. L’élève portant un t-shirt rouge est entre celui ou celle qui aime le popcorn et Nicolas (dans cet ordre)

problem.addConstraint(milieu,
                      ['popcorn', 'rouge', 'Nicolas'])


# 11. A l’une des extrémités, on retrouve l’élève qui aime les Thrillers
problem.addConstraint(extremité, ['thriller'])


# 12. Nicolas est entre Joshua et Danielle (dans cet ordre)
problem.addConstraint(milieu, [
                      'Joshua', 'Nicolas', 'Danielle'])


# 13. A la première position se trouve l’élève qui porte le t-shirt vert
problem.addConstraint(ExactSumConstraint(0), ['vert'])


solution = problem.getSolution()

# On replace le resultat dans une liste selon les positions pour pouvoir ensuite donner le resultat
liste_solution = [[], [], [], []]
pos = 0


for var in solution:
    if solution[var] == 0:
        liste_solution[0].append(var)
    if solution[var] == 1:
        liste_solution[1].append(var)
    if solution[var] == 2:
        liste_solution[2].append(var)
    if solution[var] == 3:
        liste_solution[3].append(var)

    if var == 'mms':
        pos = solution[var]

sol_mms = liste_solution[pos]


p = 0
while str(sol_mms[p]) not in prenom:
    p = p+1
name = sol_mms[p]

print('La personne qui aime les m&ms est', name)
