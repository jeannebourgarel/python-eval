from colorama import Fore, Style


def red_text(text):
    # permet d'afficher du texte en rouge
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


class Ruler:
    """classe d'objets constitués de 2 chaînes de caractères pouvant être comparées entre elles"""

    def __init__(self, chaine_1, chaine_2):
        self.chaine_1 = chaine_1
        self.chaine_2 = chaine_2
        self.matrice = [[]]
        self.alignement_1 = ''
        self.alignement_2 = ''

    def compute(self):
        """cette méthode  permet de déterminer les alignements obtenus à partir des chaînes de caractères du Ruler qui minimisent la distance"""
        chaine_1 = self.chaine_1
        chaine_2 = self.chaine_2
        a = len(chaine_1)
        b = len(chaine_2)
        # s est la matrice des coûts : une insertion, substitution ou suppression a un coût de 1
        s = [[1 for j in range(b)] for i in range(a)]
        for i in range(a):
            for j in range(b):
                if chaine_1[i] == chaine_2[j]:
                    s[i][j] = 0  # si deux lettres sont identiques : coût de 0
        # la matrice F est la matrice des scores : c'est elle qui va permettre de déterminer l'alignement de distance minimale
        F = [[0 for j in range(b+1)] for i in range(a+1)]
        for i in range(a+1):
            F[i][0] = i
        for j in range(b+1):
            F[0][j] = j
        for i in range(1, a+1):
            for j in range(1, b+1):
                # le premier terme est le score d'une substitution, le deuxième celui d'une insertion, le dernier celui d'une suppression
                F[i][j] = min(F[i-1][j-1] + s[i-1][j-1],
                              F[i][j-1] + 1, F[i-1][j] + 1)
        alignement_1 = ''
        alignement_2 = ''
        i = a
        j = b
        while i > 0 and j > 0:  # on "remonte" la matrice F pour déterminer l'alignement de distance minimale
            score = F[i][j]
            score_up = F[i-1][j]
            score_left = F[i][j-1]
            score_diag = F[i-1][j-1]
            # suppression de la lettre chaine_1[i-1] dans chaine_2
            if score == score_up + 1:
                alignement_1 = chaine_1[i-1] + alignement_1
                alignement_2 = '-' + alignement_2
                i = i-1
            elif score == score_left + 1:  # insertion dans chaine_2 d'une nouvelle lettre
                alignement_1 = '-' + alignement_1
                alignement_2 = chaine_2[j-1] + alignement_2
                j = j-1
            else:  # substitution
                alignement_1 = chaine_1[i-1] + alignement_1
                alignement_2 = chaine_2[j-1] + alignement_2
                j = j-1
                i = i-1
        while i >= 1:  # si on a finit de parcourir la chaîne 2 mais qu'il rest des lettres de la chaîne 1
            alignement_1 = chaine_1[i-1] + alignement_1
            alignement_2 = '-' + alignement_2
            i = i-1
        while j >= 1:  # c'est l'inverse : si la chaîne 1 est plus petite que la chaîne 2
            alignement_1 = '-' + alignement_1
            alignement_2 = chaine_2[j-1] + alignement_2
            j = j-1
        self.matrice = F
        self.alignement_1 = alignement_1
        self.alignement_2 = alignement_2

    def distance(self):
        """la distance est directement donnée par le terme en bas à droite de la matrice : on somme successivement les coûts minimaux"""
        return self.matrice[len(self.chaine_1)][len(self.chaine_2)]

    def report(self):
        """cette fonction permet d'afficher les deux alignements obtenus, en mettant en rouge les différences, de façon à faciliter leur comparaison"""
        alignement_1 = self.alignement_1
        alignement_2 = self.alignement_2
        a1 = ''
        a2 = ''
        for i in range(len(alignement_1)):
            a = alignement_1[i]
            b = alignement_2[i]
            if a != b:
                # on affiche en rouge les différences
                a1 = f"{a1}{red_text(a)}"
                a2 = f"{a2}{red_text(b)}"
            else:
                a1 = f"{a1}{a}"  # pas de couleur si pas de différence
                a2 = f"{a2}{b}"
        print(a1, a2)
