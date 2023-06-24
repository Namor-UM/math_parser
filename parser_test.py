import unittest
import advanced_math_parser as parser


# Тесты функции построения синтаксического дерева
class TreeTest(unittest.TestCase):
    parser = parser.Parser(parser.lex.Lexer(''))

    # Функция, сравнивающая образцовое дерево и дерево, построенное парсером.
    def tree_assert(self, example_node, tested_node):
        self.assertEqual(example_node.__class__.__name__, tested_node.__class__.__name__)
        if tested_node.__class__.__name__ == 'Operation_bin':
            self.tree_assert(example_node.left, tested_node.left)
            self.assertEqual(example_node.op, tested_node.op)
            self.tree_assert(example_node.right, tested_node.right)
        else:
            self.assertEqual(example_node.value, tested_node.value)

    # Тесты на обработку парсером единичных токенов
    def test_1layer_1(self):
        example_root = parser.Number(5)

        input = '5'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    def test_1layer_2(self):
        example_root = parser.Identifier('x')

        input = 'x'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    # Тесты на обработку парсером выражений с одним оператором
    def test_2layer_1(self):
        example_root = parser.Operation_bin('+', parser.Number(5), parser.Number(7))

        input = '5+7'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    def test_2layer_2(self):
        example_root = parser.Operation_bin('+', parser.Number(10.4), parser.Identifier('cumblast'))

        input = '10.4+cumblast'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    # Тесты на построение парсером 3-хуровневого дерева
    def test_3layer_1(self):
        sub_root = parser.Operation_bin('*', parser.Number(5), parser.Number(15))
        example_root = parser.Operation_bin('-', sub_root, parser.Number(74))

        input = '5*15-74'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    def test_3layer_2(self):
        left_sub_root = parser.Operation_bin('*', parser.Number(10), parser.Number(2.5))
        right_sub_root = parser.Operation_bin('/', parser.Number(5), parser.Number(3))
        example_root = parser.Operation_bin('==', left_sub_root, right_sub_root)

        input = '10*2.5==5/3'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    def test_3layer_3(self):
        left_sub_root = parser.Operation_bin('+', parser.Identifier('a'), parser.Identifier('b'))
        example_root = parser.Operation_bin('/', left_sub_root, parser.Number(2))

        input = '(a+b)/2'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    def test_3layer_4(self):
        left_sub_root = parser.Operation_bin('+', parser.Identifier('a'), parser.Identifier('b'))
        right_sub_root = parser.Operation_bin('-', parser.Number(5), parser.Number(3))
        example_root = parser.Operation_bin('*', left_sub_root, right_sub_root)

        input = '(a+b)*(5-3)'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)

    # Тесты на построение парсером 4-хуровневого дерева
    def test_4layer_1(self):
        right_sub_right_sub_root = parser.Operation_bin('+', parser.Number(1), parser.Number(1))
        right_sub_root = parser.Operation_bin('/', parser.Number(3), right_sub_right_sub_root)
        example_root = parser.Operation_bin('*', parser.Number(5), right_sub_root)

        input = '5*(3/(1+1))'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)
    
    def test_4layer_2(self):
        left_sub_root = parser.Operation_bin('*', parser.Number(7), parser.Number(2))
        right_sub_right_sub_root = parser.Operation_bin('/', parser.Number(140), parser.Number(4))
        right_sub_root = parser.Operation_bin('-', parser.Number(60), right_sub_right_sub_root)
        example_root = parser.Operation_bin('+', left_sub_root, right_sub_root)

        input = '7*2+(60-140/4)'
        self.parser.update_eq(input)
        tested_root = self.parser.equation()

        self.tree_assert(example_root, tested_root)
    
    # Тест обработки ошибки, возникающей при отсутствии правой скобки в пару левой.
    def test_exception_1(self):
        input = '3*(5+10'
        self.parser.update_eq(input)
        self.assertRaisesRegex(SyntaxError, 'Left bracket is unpaired!', self.parser.equation)

    # Тест обработки ошибки, возникающей при отсутствии левой скобки в пару правой.
    def test_exception_2(self):
        input = '3*5+10)'
        self.parser.update_eq(input)
        self.assertRaisesRegex(SyntaxError, 'Right bracket is unpaired!', self.parser.equation)

    # Тест обработки ошибки, возникающей при размещении оператора в несоответствующем месте.
    def test_exception_3(self):
        input = '3*/5+10'
        self.parser.update_eq(input)
        self.assertRaisesRegex(SyntaxError, 'Unexpected operation: .*', self.parser.equation)
        

# Тесты функции вычисления выражений из синтаксического дерева без переменных
class CalcTestNums(unittest.TestCase):
    parser = parser.Parser(parser.lex.Lexer(''))

    # Тесты вычисления суммы
    def test_sum_1(self):
        input = '5+35.4'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 40.4)

    def test_sum_2(self):
        input = '1.1+2.2'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 3.3)

    # Тесты вычисления разности
    def test_subtract_1(self):
        input = '47.9-100.3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), -52.4)

    def test_subtract_2(self):
        input = '15.101-4.91'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 10.191)

    # Тесты вычисления произведения
    def test_multiply_1(self):
        input = '25.33*3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 75.99)

    def test_multiply_2(self):
        input = '66*3.442'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 227.172)

    # Тесты вычисления частного
    def test_divide_1(self):
        input = '36/3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 12)

    def test_divide_2(self):
        input = '36.9/3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 12.3)

    # Тесты вычисления равенства
    def test_equality_1(self):
        input = '15==17-2'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), True)

    def test_equality_2(self):
        input = '1.1+2.2==3.3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), True)


# Тесты функции вычисления выражений из синтаксического дерева с переменными
class CalcTestVars(unittest.TestCase):
    parser = parser.Parser(parser.lex.Lexer(''))

    # Тесты вычисления суммы
    def test_sum_1(self):
        input_list = ['a=5']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = 'a+35.4'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 40.4)

    def test_sum_2(self):
        input_list = ['boolka=2.2']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = '1.1+boolka'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 3.3)

    # Тесты вычисления разности
    def test_subtract_1(self):
        input_list = ['a=0.9']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = '47+a-100.3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), -52.4)

    def test_subtract_2(self):
        input_list = ['b=4.91']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = '15.101-b'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 10.191)

    # Тесты вычисления произведения
    def test_multiply_1(self):
        input_list = ['a=36/6*2/4']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = '25.33*a'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 75.99)

    def test_multiply_2(self):
        input_list = ['b=33*2']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = 'b*3.442'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 227.172)

    # Тесты вычисления частного
    def test_divide_1(self):
        input_list = ['a=6*6', 'b=a/12']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = 'a/b'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 12)

    def test_divide_2(self):
        input_list = ['c=3']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = '36.9/c'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), 12.3)

    # Тесты вычисления равенства
    def test_equality_1(self):
        input_list = ['a=2.5*2', 'b=60/2']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = '3*(5+a)==b/3+5*4'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), True)

    def test_equality_2(self):
        input_list = ['a=1.1', 'b=a*2']
        for input in input_list:
            self.parser.update_eq(input)
            self.parser.equation().calc()
        input = 'a+b==3.3'
        self.parser.update_eq(input)
        self.assertEqual(self.parser.equation().calc(), True)

    # Тест на обработку ошибки, связанной с использованием в выражениях необъявленной переменной
    def test_exception_1(self):
        input = '3*balls+10'
        self.parser.update_eq(input)
        self.assertRaisesRegex(SyntaxError, r'Identifier .+ is not defined!', self.parser.equation().calc)


if __name__ == '__main__':
    unittest.main()