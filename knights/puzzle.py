from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentenceA = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    #If sentence A is false the AKnave is true
    # If sentence A is true the AKnight is true
    Implication(sentenceA, AKnight),
    Implication(Not(sentenceA), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
sentenceA = And(AKnave, BKnave)
# B says nothing.

knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Implication(sentenceA, AKnight),  # If A is a knave, then A is a knight
    Implication(Not(sentenceA), AKnave),  # If A is not a knave, then A is a knave
    Implication(AKnave, BKnight),  # If A is a knave, then B is a knight
    Implication(AKnight, BKnave)  # If A is not a knave, then B is a knave
)

# Puzzle 2
# A says "We are the same kind."
sentenceA = Or( And(AKnight, BKnight) , And(AKnave, BKnave) )
# B says "We are of different kinds."
sentenceB = Or( And(AKnight, BKnave) , And(AKnave, BKnight) )
knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Implication(sentenceA, AKnight),  # If A is a knave, then A is a knight
    Implication(Not(sentenceA), AKnave),  # If A is not a knave, then A is a knave
    Implication(sentenceB, BKnight),  # If B is a knave, then B is a knight
    Implication(Not(sentenceB), BKnave),  # If B is not a knave, then B is a knave
    Implication(BKnight, AKnave),
    Implication(AKnight, BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentenceA = Or(AKnight, AKnave)
# B says "A said 'I am a knave'."

# B says "C is a knave."
sentenceB1 = AKnave
sentenceB =  CKnave
# C says "A is a knight."
sentenceC = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Or(CKnight, CKnave),  # C is either a knight or a knave
     
    Implication(sentenceB, And(BKnight,CKnave)),
    Implication(Not(sentenceB), And(BKnave, CKnight)),

    Implication(sentenceC, And(CKnight, AKnight)),
    Implication(Not(sentenceC), And(CKnave, AKnave)),

    Implication(BKnight, sentenceB1),
    Implication(BKnave, Not(sentenceB1)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
   main()