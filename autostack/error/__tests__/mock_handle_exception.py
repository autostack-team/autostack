'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/23/2019
Overview: Mocks the handle_exception function.
'''


class MockHandleException:
    '''
    Mocks the handle_exception function.
    '''

    def __init__(self):
        '''
        Initializes a mock handle_exception with was_called set
        to False and parameter set to None.
        '''

        self.was_called = False
        self.parameter = None

    def handle_exception(self, error):
        '''
        Sets was_called to True, indicating that the function was
        called, and parameter is set to the error string passed into
        the function.
        '''

        self.was_called = True
        self.parameter = error
