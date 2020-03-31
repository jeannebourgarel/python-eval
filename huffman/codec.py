class TreeBuilder:
    """cette classe permet de construire un arbre de Huffman à partir d'un texte"""

    def __init__(self, text):
        self.text = text

    def tree(self):
        text = self.text
        # dictionnaire {lettre : nombre d'occurences de lettre}
        occurences = {a: text.count(a) for a in text}
        lettres = sorted(occurences.items(), key=lambda t: t[1])
        # liste des lettres triée par ordre croissant d'occurrences
        lettres = [x for (x, y) in lettres]
        # nombre d'occurences de la première lettre de la liste 'lettres'
        m = occurences[lettres[0]]
        ligne_sup = []  # arbre : [[gauche : 0],[droite : 1 ],'abc', 26] par exemple
        while m < len(text):  # m = le nombre de lettres du texte qu'on a "classée" dans l'arbre
            # on commence l'arbre par les "feuilles", pour remonter jusqu'à la racine
            ligne_inf = ligne_sup[:]
            ligne_sup = []
            if lettres != []:
                a = lettres.pop(0)
                x = occurences[a]
                while x <= m and lettres != []:
                    ligne_inf.append([[], [], a, x])
                    a = lettres.pop(0)
                    x = occurences[a]
                # chaque étage de l'arbre doit contenir un nombre impair d'éléments de texte
                if len(ligne_inf) % 2 == 1:
                    ligne_inf.append([[], [], a, x])
                else:
                    lettres = [a] + lettres
            long = len(ligne_inf)
            if long > 1:
                # on construit la ligne supérieure en sommant deux à deux chaque "feuille"
                for i in range(0, long - 1, 2):
                    gauche = ligne_inf[i]
                    droite = ligne_inf[i+1]
                    ligne_sup.append(
                        [gauche, droite, gauche[2] + droite[2], gauche[3] + droite[3]])
                if long % 2 == 1:
                    ligne_sup.append(ligne_inf[-1])
            m = max([l[3] for l in ligne_sup])
        return ligne_sup[0]


class Codec:
    """cette classe permet de coder un texte, et de décoder un code, à partir d'un arbre de Huffman donné (qui doit correspondre au texte"""

    def __init__(self, tree):
        self.tree = tree

    def encode(self, text):
        res = ''
        tree = self.tree
        for a in text:
            # tree[2] contient toutes les lettres du texte à partir duquel on l'a construit
            if a not in tree[2]:
                return 'incodable'
            else:
                # on va coder la lettre a par une suite de 0 et de 1 définie à partir de sa position dans tree
                L = tree[:]
                while len(L[2]) > 1:
                    gauche, droite = L[0], L[1]
                    if a in gauche[2]:
                        res = res + '0'
                        L = L[0]
                    else:
                        res = res + '1'
                        L = L[1]
        return res

    def decode(self, code):
        res = ''
        tree = self.tree
        L = tree[:]
        for k in code:
            i = eval(k)
            L = L[i]
            if len(L[2]) == 1:  # on parcourt l'arbre selon la suite de 0 et de 1 jusqu'à trouver une lettre, et on recommence
                res += (L[2])
                L = tree[:]
        return res
