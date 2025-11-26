from logic import *

# Global symbols required for check50
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# --- Helper Rules ---
# Basic game rules: Each character is either a Knight or a Knave, not both.
rule_A = And(Not(And(AKnight, AKnave)), Or(AKnight, AKnave))
rule_B = And(Not(And(BKnight, BKnave)), Or(BKnight, BKnave))
rule_C = And(Not(And(CKnight, CKnave)), Or(CKnight, CKnave))

# Puzzle 0
# A says "I am both a knight and a knave."
statement_p0 = And(AKnight, AKnave)
puzzle0_logic = And(
    rule_A,
    Implication(AKnight, statement_p0),
    Implication(AKnave, Not(statement_p0))
)
knowledge0 = puzzle0_logic


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement_p1_A = And(AKnave, BKnave)
puzzle1_logic = And(
    rule_A,
    rule_B,
    # A's statement logic
    Implication(AKnight, statement_p1_A),
    Implication(AKnave, Not(statement_p1_A))
)
knowledge1 = puzzle1_logic


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
statement_p2_A = And(AKnight, BKnight) # If A is Knight, "Same kind" means B is also Knight
statement_p2_B = And(BKnight, AKnave)  # If B is Knight, "Different" means A is Knave

puzzle2_logic = And(
    rule_A,
    rule_B,
    # A's statement logic
    Implication(AKnight, statement_p2_A),
    Implication(AKnave, Not(And(AKnave, BKnave))), # If A is Knave, "Same" (Knave+Knave) is False

    # B's statement logic
    Implication(BKnight, statement_p2_B),
    Implication(BKnave, Not(And(BKnave, AKnight))) # If B is Knave, "Different" (Knave+Knight) is False
)
knowledge2 = puzzle2_logic


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# Logic for A said "I am a knight"
a_said_knight = And(
    Implication(AKnight, AKnight),
    Implication(AKnave, Not(AKnight))
)

# Logic for A said "I am a knave"
a_said_knave = And(
    Implication(AKnight, AKnave),
    Implication(AKnave, Not(AKnave))
)

puzzle3_logic = And(
    rule_A,
    rule_B,
    rule_C,

    # A says either "I am a knight." or "I am a knave."
    Or(a_said_knight, a_said_knave),
    # But not both (implied by the exclusive statements, but added for rigor)
    Not(And(a_said_knight, a_said_knave)),

    # B says "A said 'I am a knave'."
    Implication(BKnight, a_said_knave),
    Implication(BKnave, Not(a_said_knave)),

    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)
knowledge3 = puzzle3_logic


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