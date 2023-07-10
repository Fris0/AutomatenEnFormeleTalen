# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from FA import FA
import string
import sys


def create_fa():
    """
    Creates the finite automaton (FA) for trace tokenization
    Characters for left endmarker and BLANK: ⊢ , ⊔
    """

    Q = ['START', 'SPACE', 'MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM',
         'SYMBOL']
    Sigma = [' ', '<', '>', "-", "+", '⊔', '⊢', 'character', 'digit']
    delta = {'START': {' ': 'SPACE',
                       '<': 'MLEFT',
                       '>': 'MRIGHT',
                       '+': 'WRITE',
                       '-': 'READ',
                       '⊔': 'BLANK',
                       '⊢': 'LEM',
                       'character': 'SYMBOL',
                       'digit': 'SYMBOL'},
             'SYMBOL': {'character': 'SYMBOL',
                        'digit': 'SYMBOL'}}
    s = 'START'
    F = ['SPACE', 'MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']

    M = FA(Q, Sigma, delta, s, F, verbose=False)

    return M


def char_type(char):
    """
    Returns the type of a character found in the trace
    """
    if char in string.digits:
        return (True, 'digit')
    elif char in string.ascii_letters:
        return (True, 'character')
    else:
        return (False, char)


def lexer(fa, trace):
    """
    The lexer iterates through the trace, tokenizing and assigning states to it
    fa: The finite automaton
    trace: A single string
    returns: A list of tuples containing first the token then the state.
    If something goes wrong the function should call sys.exit()
    """

    """
    The lexer is implemented by looping over the elements of a trace
    until it's empty. In the loop
    the fa will be reset when the automata is in a final
    state AND is not the SYMBOL state, therefore continuing the
    tokenization. When there are no more symbols to
    tokenize, the loop will stop. An exception is when
    a symbol is found which is not in Sigma, then
    sys.exit() call will be made.
    """

    fa.reset()
    token = []
    while (trace):
        if char_type(trace[0]):
            fa.reset()

        step = fa.transition(char_type(trace[0])[1])
        if step is False:
            sys.exit()
        else:
            token.append((trace[0], fa.state_val()))
            trace = trace[1:]

    else:
        return token


def main(path):
    """
    Reads multiple traces from the file at 'path' and feeds them one by one to
    the lexer.
    """
    M = create_fa()

    fo = open(path, encoding='utf-8')
    with fo as f:
        traces = [line.rstrip('\n') for line in f]
    fo.close()

    for trace in traces:
        M.reset()
        print("Trace : \"" + trace + "\"")
        print("Lexer : " + str(lexer(M, trace)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 lexer.py traces.txt`')
    source = sys.argv[1]
    main(source)
