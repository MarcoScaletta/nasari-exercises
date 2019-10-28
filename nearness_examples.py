
from nasari import Nasari

nasari = Nasari("dd-small-nasari-15.txt")

print(nasari.sim("weapon", "fire"))

bow1 = {'nuclear', 'problem', 'weapon'}
bow2 = {'fire', 'gun', 'solution'}

print(nasari.nearness(bow1, bow2))
