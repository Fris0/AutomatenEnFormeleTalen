# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


from TM import TM
import sys


def is_input(a):
    if a.isdigit():
        return True
    elif a.isalpha():
        return True
    elif a == '|':
        return True
    else:
        return False


def is_output(a):
    if a.isdigit():
        return True
    elif a.isalpha():
        return True
    elif a == '⊔' or a == '⊢':
        return True
    elif a == '|':
        return True
    else:
        return False


def extract_input(trace, trace_tokenized=None):
    """
    Determines (and returns) the input string given to the TM that caused it to
    perform the computation that produced the given trace.
    trace:            a single TM trace (as a string with spaces).
    trace_tokenized:  optional, the same trace tokenized (as a list of tokens).
    returns:          the input (as a string without spaces)
    """

    # Explenation:
    # First the trace is split into sizes of 5. Which we call
    # chunks. These chunks are then iterated over one by one.
    # Then there is an equilibrium variable, which
    # grows negative everytime the trace decides to move to the left
    # When the equilibrium variable is 0 again,
    # it then will take into account the input at an index.
    # We also check if the value which is at an indexed position conforms
    # to the input by using the self built is_input function.

    # Characters for left endmarker and BLANK: ⊢ , ⊔

    trace = (trace.split(' '))

    chunks = [trace[i:i + 5] for i in range(0, len(trace), 5)]

    output = ["@"] * len(chunks)

    eq = 0
    # 0 means the track is in equilibrium.
    # Inbalanced equilibrium means no inputs will be taken into account.

    for i, chunk in enumerate(chunks):
        if eq == 0:
            if is_input(chunk[1]):
                output[i] = chunk[1]
            if chunk[4] != '>':
                eq -= 2
        else:
            if chunk[4] != '<':
                eq += 1
            else:
                eq -= 1

    output = list((filter(lambda output: is_input(output), output)))
    return ''.join(output)


def filter_blanks(input):
    while (input[len(input) - 1] == "⊔"):
        input = input[: (len(input) - 1)]
    return (input)


def extract_output(trace, trace_tokenized=None):
    """
    Determines (and returns) the tape output produced by the TM when performing
    the computation that produced the given trace. The ouput is the longest
    possible string _after_ the left endmarker that does not end in
    a BLANK ('⊔').
    trace:            a single TM trace (as a string with spaces).
    trace_tokenized:  optional, the same trace tokenized (as a list of tokens).
    returns:          the output (as a string without spaces)
    """

    # Explenation:
    # First the trace is split into sizes of 5. Which we call
    # chunks. These chunks are then iterated over one by one.
    # Every cycle we keep track of the idx, which
    # can grow negatively and positively, but is always larger
    # than or equal to 0.
    # At every location the output string is idx with the current idx value
    # and the value is stored.
    trace = (trace.split(' '))

    chunks = [trace[i:i + 5] for i in range(0, len(trace), 5)]

    output = ["@"] * len(chunks)

    idx = 0

    for i, chunk in enumerate(chunks):
        output[idx] = chunk[3]
        if chunk[4] == '>':
            idx += 1
        else:
            idx -= 1

    output = output[1:]
    output = list((filter(lambda output: is_output(output), output)))

    return "".join(filter_blanks(output))


def reverse_manually():
    """
    The original TM was designed to:

    It looks at an even sized digit string at both sides, and
    performs an exclusive or (XOR) operation.

    The algorithm used by the original TM works as follows:

    It receives a string split in half by the "|" marker
    and uses the "|" marker to store the number selected on the left handside.
    It then takes a number on the right hand side, and if the numbers in the
    position of the "|" marker is not equal to the one on the right hand side
    then a 1 will be placed at the left hand side, and otherwise 0. It also
    puts a "⊔" marker everytime it picks the most left handside number
    which it later replaces with the outcome of the equality check,
    and the right hand side will stay the same to the "⊔" marker
    after it has been read.

    Thus going from:
    ⊢ 1 0 0 1 1 | 0 0 0 0 1 ⊔ ⊔ ⊔ ...

    to:
    ⊢ 1 0 0 1 0 ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ...

    Returns: A TM object of no more than 20 states, capable of reproducing the
             traces given by the assignment.
    """

    # Explenation:
    # The algorithm of the original TM is implemented as followed.
    # It starts by reading the left end mark symbol, and moves to the right.
    # It then moves to state 1, where it reads the first digit it will find,
    # places a bucket (⊔) symbol, and goes to the corresponding state,
    # depending on 0 or 1. This is needed, because we need to know,
    # which symbol to play in the split (|) symbol, thus two different
    # behaviours. All other digits met by state 2 and 3 on their
    # way to the split symbol are replaced with the same digit.
    # When the split symbol has been replaced with the symbol
    # it has read on the left hand side, both state 2 and 3
    # will go into state 4. In state 4 it also continues
    # to move to the right, until it has found a digit.
    # It then goes into state 5 and 6, based on the symbol
    # which was found on the right hand side. This is needed
    # because if the symbol in the middle is different
    # to the one that is read on the right hand side,
    # then it requires different behaviours. So, if the
    # the symbol on the right side which is read is not the same as the one
    # which has been grabbed on the left side, then it goes into state 7.
    # Else into state 8. State 7 and 8 then move to the spot where the bucket
    # is and place either 0 or 1. 0 if the symbol at the split symbol
    # was even, and else 1. Then it moves back to the right, and starts from
    # state 1 again, until state 1 starts at the split symbol after a cycle.

    Q = ['t', 'r', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    Sigma = ['0', '1', '|']
    Gamma = ['0', '1', '|', '⊔', '⊢']
    delta = [(('s0', '⊢'), ('s1', '⊢', 'R')),
             (('s1', '0'), ('s2', '⊔', 'R')),
             (('s1', '1'), ('s3', '⊔', 'R')),
             (('s1', '|'), ('t', '⊔', 'R')),

             (('s2', '0'), ('s2', '0', 'R')),
             (('s2', '1'), ('s2', '1', 'R')),

             (('s3', '0'), ('s3', '0', 'R')),
             (('s3', '1'), ('s3', '1', 'R')),

             (('s2', '|'), ('s4', '0', 'R')),
             (('s3', '|'), ('s4', '1', 'R')),

             (('s4', '⊔'), ('s4', '⊔', 'R')),
             (('s4', '1'), ('s5', '⊔', 'L')),
             (('s4', '0'), ('s6', '⊔', 'L')),

             (('s5', '⊔'), ('s5', '⊔', 'L')),
             (('s5', '1'), ('s7', '|', 'L')),
             (('s5', '0'), ('s8', '|', 'L')),

             (('s6', '⊔'), ('s6', '⊔', 'L')),
             (('s6', '0'), ('s7', '|', 'L')),
             (('s6', '1'), ('s8', '|', 'L')),

             (('s7', '0'), ('s7', '0', 'L')),
             (('s7', '1'), ('s7', '1', 'L')),
             (('s7', '⊔'), ('s1', '0', 'R')),

             (('s8', '0'), ('s8', '0', 'L')),
             (('s8', '1'), ('s8', '1', 'L')),
             (('s8', '⊔'), ('s1', '1', 'R')),
             ]
    s = 's0'
    t = 't'
    r = 'r'

    tm = TM(Q, Sigma, Gamma, delta, s, t, r, verbose=True)

    return tm


def reverse_generic(traces, traces_tokenized=None):
    """
    Recreates (reverse-engineers) a TM which behaves identically to the TM that
    produced the supplied list of traces. Note: 'behaves identically' implies
    that the recreated TM must produce (given the same input) the exact same
    execution traces as the original.
    traces:           a list of traces produced by the original TM.
    traces_tokenized: optional, tokenized versions of the original traces.
    returns:          a TM object capable of reproducing the traces given
                      the same input.
    """

    # Your code + explanation here

    Q = ['t', 'r']
    Sigma = []
    Gamma = ['⊔', '⊢']
    delta = []
    s = ''
    t = 't'
    r = 'r'

    tm = TM(Q, Sigma, Gamma, delta, s, t, r, verbose=True)

    return tm


def main(path_traces=None, path_tokenized=None):
    """
    Area to test different parts of your implementation.

    The present code is just an example, feel free to modify at will.
    While it is strongly recommended to write some tests here, the code
    produced will not directly influence your grade.
    """

    """ Input/output extraction """
    test_traces = [
                  '- ⊢ + ⊢ > - 0 + 1 > - 0 + 1 < - 1 + ⊔ > - 1 + ⊔ > - ⊔ + a '
                  '>',
                  '- ⊢ + ⊢ > - a + ⊢ < - ⊢ + ⊢ > - ⊢ + ⊔ > - b + ⊔ < - ⊔ '
                  '+ ⊢ > - ⊔ + ⊔ > - ⊔ + ⊢ <'
                  ]

    correct_inputs = [
                      '00',
                      'ab'
                     ]

    correct_outputs = [
                       '⊔⊔a',
                       '⊢⊔⊢'
                      ]

    # Only test input/output extraction functions that do not return "None"
    for idx in range(len(test_traces)):
        feedback = ""
        extracted_input = extract_input(test_traces[idx])
        if extracted_input is not None and \
           extracted_input != correct_inputs[idx]:
            feedback += "\nextracted input: \'" + extracted_input + "\'"\
                        "incorrect! (expected: \'" + correct_inputs[idx]\
                        + "\')"
        extracted_output = extract_output(test_traces[idx])
        if extracted_output is not None and \
           extracted_output != correct_outputs[idx]:
            feedback += "\nextracted output: \'" + extracted_output + "\'"\
                        "incorrect! (expected: \'" + correct_outputs[idx]\
                        + "\')"
        if feedback:
            feedback = test_traces[idx] + feedback
            print(feedback)

    """ Reverse engineering """
    # Read execution traces (as strings with spaces), if available.
    # if path_traces:
    #    fo = open(path_traces, encoding='utf-8')
    #    with fo as f:
    #        traces = [trace for trace in [line.rstrip('\n') for line in f]]
    #    fo.close()

    # Read tokenized traces (as lists of tokens, excluding 'SPACE'),
    # if available.
    # if path_tokenized:
    #    fo = open(path_tokenized, encoding='utf-8')
    #    with fo as f:
    #        traces_tokenized = [trace.split() for trace in [line.rstrip('\n')
    #                            for line in f]]
    #    fo.close()

    # Scratchpad, try to Reverse engineer the TM using the framework!

    # for i in traces:
    #   print(i)
    #   print("input", extract_input(i))
    #   print("output", extract_output(i))
    # TM.visualize(extract_input(i), i)

    # Validate your solution by checking if it produces the original traces
    # given the original inputs...

    # tm = reverse_manually()
    # for trace in traces:
    #    tm.set_input(extract_input(trace))
    #    tm.transition_all()
    #    produced_trace = tm.get_execution_trace()
    #    if trace != produced_trace:
    #        print("TM produced an incorrect trace!")
    #        print("original: " + trace)
    #        print("TM:       " + produced_trace)
    #        input("Press enter to continue...")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        path_traces = sys.argv[1]
        path_tokenized = sys.argv[2]
        main(path_traces, path_tokenized)
    elif len(sys.argv) > 1:
        path_traces = sys.argv[1]
        main(path_traces)
    else:
        main()
