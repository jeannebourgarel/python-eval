from argparse import ArgumentParser
from ruler import Ruler
parser = ArgumentParser()
parser.add_argument("fichier", help="le nom du fichier")
args = parser.parse_args()
print(args.fichier)

with open(args.fichier, 'r') as f:
    L = []
    for line in f:
        L.append(line.strip())
    n = len(L)
for k in range(0, n - 1, 2):
    ruler = Ruler(L[k], L[k + 1])
    ruler.compute()
    print(f"=== exemple #{k//2 + 1} - distance = {ruler.distance()}")
    print(ruler.report())
