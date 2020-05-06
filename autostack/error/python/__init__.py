'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/13/2019
Overview: Ability to parse output for python error messages.
'''

from autostack.error.python.constants import SYNTAX_ERRORS


def parse_output_for_error(output, pipe):
    '''
    Parses a line of output, and determines whether or not it is
    an error message. There are two types of errors, syntax errors
    and runtime errors. Syntax errors do not have a traceback but
    runtime errors do.

    e.g. without traceback:
        IndentationError: unexpected indent
    e.g. with traceback:
        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
        NameError: name 'xyz' is not defined

    Parameter {str} output: line of output from a pipe.
    Parameter {File} pipe: pipe to read output from, in case of traceback.
    Returns {string|None}: the error, or None, if it's not an error.
    '''

    try:
        # Syntax errors - no traceback.
        if output.split()[0][:-1] in SYNTAX_ERRORS:
            error = output.split()[0][:-1]
            return error
        # Runtime error - has traceback.
        elif 'Traceback' in output.split():
            error = get_error_from_traceback(pipe)
            return error
    except IndexError:
        pass
    
    return None


def get_error_from_traceback(pipe):
    '''
    Gets the error description from a traceback.

    e.g.:
        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
        NameError: name 'xyz' is not defined
    would return 'NameError'.

    Parameter {File} pipe: the pipe to read the traceback from.
    Returns {str}: the error description.
    '''

    output = pipe.readline()

    while (
            output.split()[0][-1] != ':'
    ):
        output = pipe.readline()

    return output.split()[0][:-1]
