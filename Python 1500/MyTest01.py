#!/usr/bin/env python3

def add(num_a, num_b):
    ''' Add two basic types.
    >>> add(321, 123)
    444
    >>> add("321", "123")
    '321123'
    '''
    return num_a + num_b

if __name__ == '__main__':
    import doctest
    doctest.testmod()

