# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PDA import PDA
import sys


def verify_movement(trace):
    """
    Creates and uses a PDA to verify proper Turing machine (TM) movement in a
    single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    # Characters for initial stack symbol and epsilon: ⊥ , ϵ

    # Explanation:
    # Adds a right (>) symbol to the stack when moving to the right
    # and removes it from the stack when moving to the left.
    # If the trace is valid, then the stack will be
    # greater than 0 at the end. When it tries to
    # go below size 0, it will go into fail state,
    # and never enter the finished state.

    Q = ["S1", "S2", "FS"]  # Where FS stand for Failed State
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']
    Gamma = [">", "⊥"]  # Stack alphabet to keep track of right movements
    delta = [(("S1", "MLEFT", "⊥"), ("FS", "ϵ")),
             (("S1", "MRIGHT", "⊥"), ("S2", ">")),
             (("S2", "MRIGHT", ">"), ("S2", [">", ">"])),
             (("S2", "MLEFT", ">"), ("S2", "ϵ")),
             (("S2", "MLEFT", "ϵ"), ("FS", "ϵ"))]
    s = "S1"
    F = ["S2"]
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=True)

    # Note: you can use my_pda.transition(symbol) to test a single transition.

    return my_pda.transition_all(trace)


def verify_lem(trace):
    """
    Creates and uses a PDA to verify Turing machine (TM) left endmarker for a
    single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    # Characters for initial stack symbol and epsilon: ⊥ , ϵ
    # Explenation:
    # Uses finite automata to check if
    # the first symbol that is read is
    # actually the LEM symbol. After that,
    # it will enter the PDA of the type final state.
    # In this PDA there are 3 states. State 6 checks
    # if the turing machine doesn't surpass the LEM symbol
    # by moving left. State 7 checks that the LEM symbol
    # is not replaced by a distinct symbol and
    # that the PDA moves right. State 8 checks that
    # when the move right symbol is read, that it
    # is only replaced by the same symbol or
    # LEM symbol. After that it makes sure, that
    # if the LEM symbol is written, it moves to the right.
    # Else it is allowed to move left. But that will be checked
    # in state 6. Thus this rule was not necessary in state 8.
    #
    # Addition: A move right symbol will be placed, when it has moved right.

    # In states the FS is the failed STATE
    Q = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "FS"]
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']
    Gamma = ["⊢", ">", "ϵ", "⊥"]
    delta = [(("S1", "READ", "⊥"), ("S2", "ϵ")),

             (("S2", "LEM", "ϵ"), ("S3", "ϵ")),
             (("S2", "SYMBOL", "ϵ"), ("FS", "ϵ")),
             (("S2", "BLANK", "ϵ"), ("FS", "ϵ")),

             (("S3", "WRITE", "ϵ"), ("S4", "ϵ")),

             (("S4", "LEM", "ϵ"), ("S5", "⊢")),
             (("S4", "SYMBOL", "ϵ"), ("FS", "ϵ")),
             (("S4", "BLANK", "ϵ"), ("FS", "ϵ")),

             (("S5", "MRIGHT", "⊢"), ("S6", [">", "⊢"])),
             (("S5", "MLEFT", "⊢"), ("FS", "ϵ")),

             (("S6", "MLEFT", ">"), ("S6", "ϵ")),
             (("S6", "MLEFT", "⊢"), ("FS", "ϵ")),
             (("S6", "MRIGHT", ">"), ("S6", [">", ">"])),
             (("S6", "MRIGHT", "⊢"), ("S6", [">", "⊢"])),

             (("S6", "READ", "⊢"), ("S7", "⊢")),
             (("S7", "BLANK", "⊢"), ("FS", "ϵ")),
             (("S7", "SYMBOL", "⊢"), ("FS", "ϵ")),
             (("S7", "MRIGHT", "⊢"), ("S6", "⊢")),
             (("S7", "MLEFT", "⊢"), ("FS", "ϵ")),

             (("S6", "READ", ">"), ("S8", ">")),
             (("S8", "LEM", ">"), ("S8", "⊢")),
             (("S8", "MRIGHT", "⊢"), ("S6", "⊢")),
             (("S8", "MLEFT", "⊢"), ("FS", "ϵ")),
             (("S8", "BLANK", ">"), ("FS", "ϵ")),
             (("S8", "SYMBOL", ">"), ("S6", ">")),
             ]

    s = 'S1'
    F = ["S6"]
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=True)

    # Note: you can use my_pda.transition(symbol) to test a single transition.

    return my_pda.transition_all(trace)


def main(path):
    """
    Reads multiple tokenized traces from the file at 'path' and feeds them to
    the various verification functions.
    """
    # Read and parse traces.
    fo = open(path, encoding='utf-8')
    with fo as f:
        traces = [trace.split() for trace in [line.rstrip('\n') for line in f]]
    fo.close()

    # Verify traces using verification functions
    valid = traces
    for trace in valid:
        print("Trace          : \"" + str(trace) + "\"")
        print("Verify movement: " + str(verify_movement(trace)))
    valid = [trace for trace in valid if verify_movement(trace)]
    for trace in valid:
        print("Trace          : \"" + str(trace) + "\"")
        print("Verify LEM     : " + str(verify_lem(trace)))
    valid = [trace for trace in valid if verify_lem(trace)]

    # Print the remaining valid trace(s)
    print("Remaining trace(s):")
    for trace in valid:
        print(trace)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 verification.py \
                 tokenized_traces.txt`')
    source = sys.argv[1]
    main(source)
