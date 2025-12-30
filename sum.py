import sys

# Expect 2 arguments
if len(sys.argv) != 3:
    print("Erreur: Deux arguments sont nécessaires.")
    sys.exit(1)

try:
    a = float(sys.argv[1])
    b = float(sys.argv[2])
except ValueError:
    print("Erreur: Les arguments doivent être des nombres.")
    sys.exit(1)

result = a + b
print(result)
