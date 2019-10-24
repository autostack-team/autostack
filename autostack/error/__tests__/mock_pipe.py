'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/23/2019
Overview: Mocks a pipe.
'''


class MockPipe:
    '''
    Mocks a pipe.
    '''

    def __init__(self, readline_returns=''):
        '''
        Initializes a mock pipe with readline return values and
        the number of readline calls set to 0.
        '''

        self.readline_returns = readline_returns
        self.readline_call_count = 0

    def readline(self):
        '''
        Returns a value for readline, based on the current call
        count value.
        '''

        readline_val = self.readline_returns[self.readline_call_count]
        self.readline_call_count += 1
        return readline_val

    def get_readline_call_count(self):
        '''
        Returns the readline method call count.
        '''

        return self.readline_call_count
