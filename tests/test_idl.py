import unittest

from dooble.idl import Idl


class TestIdl(unittest.TestCase):
    def test_empty_observable(self):
        text = '----->'

        expected_result = [[
            [],
            [ 
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
            ],
            '>'
        ]]

        idl = Idl()
        ast = idl.parse(text)
        self.assertEqual(expected_result, ast)

    def test_observable_items(self):
        text = '-a-b-c-->'

        expected_result = [[
            [], 
            [ 
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'a'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'b'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'c'},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
            ],
            '>'
        ]]


        idl = Idl()
        ast = idl.parse(text)
        print(ast)
        self.assertEqual(expected_result, ast)

    def test_observable_skipspan(self):
        text = '  -a-b-c-->'

        expected_result = [[
            [' ', ' '],
            [ 
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'a'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'b'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'c'},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
            ],
            '>'
        ]]


        idl = Idl()
        ast = idl.parse(text)
        print(ast)
        self.assertEqual(expected_result, ast)


    def test_observable_completed(self):
        text = '-a-b-c--|'

        expected_result = [[
            [],
            [ 
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'a'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'b'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'c'},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
            ],
            '|'
        ]]


        idl = Idl()
        ast = idl.parse(text)
        print(ast)
        self.assertEqual(expected_result, ast)


    def test_observable_error(self):
        text = '-a-b-c--*'

        expected_result = [[
            [],
            [ 
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'a'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'b'},
                {'ts': '-', 'item': None},
                {'ts': None, 'item': 'c'},
                {'ts': '-', 'item': None},
                {'ts': '-', 'item': None},
            ],
            '*'
        ]]


        idl = Idl()
        ast = idl.parse(text)
        print(ast)
        self.assertEqual(expected_result, ast)

    def test_operator(self):
        text = '[ map(i: i*2) ]'

        expected_result = [{ 'op': [
            '[',
            ' map(i: i*2) ',
            ']'
        ]}]


        idl = Idl()
        ast = idl.parse(text)
        print(ast)
        self.assertEqual(expected_result, ast)
