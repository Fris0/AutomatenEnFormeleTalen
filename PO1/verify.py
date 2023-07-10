# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from FA import FA
import lexer as lexer
import sys


def create_fa():
    """
    Creates the finite automaton (FA) for step verification
    Characters for left endmarker and BLANK: ⊢ , ⊔
    """

    Q = ['START', 'S1', 'S2', 'S3', 'S4', 'S5']
    Sigma = ['SPACE', 'MLEFT', 'MRIGHT', 'READ',
             'WRITE', 'BLANK', 'LEM', 'SYMBOL']
    delta = {'START': {'READ': 'S1',
                       'SPACE': 'START'},
             'S1': {'SYMBOL': 'S2',
                    'LEM': 'S2',
                    'BLANK': 'S2',
                    'SPACE': 'S1'},
             'S2': {'WRITE': 'S3',
                    'SPACE': 'S2'},
             'S3': {'SYMBOL': 'S4',
                    'LEM': 'S4',
                    'BLANK': 'S4',
                    'SPACE': 'S3'},
             'S4': {'MLEFT': 'S5',
                    'MRIGHT': 'S5',
                    'SPACE': 'S4'},
             'S5': {'READ': 'S1',
                    'SPACE': 'S5'}}

    s = 'START'
    F = ['START', 'S5']

    M = FA(Q, Sigma, delta, s, F, verbose=False)

    return M


def verify_steps(fa, lexed_trace):
    """
    The verification function steps through the lexed trace and feeds the token
    portion of tuple to the fa. Either filter out SPACE tokens or adjust the FA
    fa: The finite automaton
    lexed_trace: A list of tuples of the form (event, token).
    returns: True if the trace is valid, false otherwise.
    """
    fa.reset()
    steps = [step[1] for step in lexed_trace]
    for step in steps:
        result = fa.transition(step)
        if (not result):
            return False

    if (fa.is_final() is True):
        return True
    else:
        False


def main(path):
    """
    Reads multiple traces from the file at 'path' and feeds them first to the
    lexer and then to verify_steps.
    """

    fo = open(path, encoding='utf-8')
    with fo as f:
        traces = [line.rstrip('\n') for line in f]
    fo.close()

    M_lexer = lexer.create_fa()
    M_verify = create_fa()

    for trace in traces:
        M_lexer.reset()
        M_verify.reset()
        print("Trace : \"" + trace + "\"")
        lexed_trace = lexer.lexer(M_lexer, trace)
        print("Lexer : " + str(lexer.lexer(M_lexer, trace)))
        print("Verify: " + str(verify_steps(M_verify, lexed_trace)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 verify.py traces.txt`')
    source = sys.argv[1]
    main(source)
