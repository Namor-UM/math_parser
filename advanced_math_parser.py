import advanced_math_lexer as lex


id_value_dict = {}


class Node:
    pass


class Operation_bin(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    
    def __repr__(self):
        return f'{self.op}({self.left}, {self.right})'
    

    def calc(self):
        match self.op:
            case '+':
                return self.left.calc() + self.right.calc()
            case '-':
                return self.left.calc() - self.right.calc()
            case '*':
                return self.left.calc() * self.right.calc()
            case '/':
                return self.left.calc() / self.right.calc()
            case '==':
                return self.left.calc() == self.right.calc()
            case '=':
                if type(self.left).__name__ == 'Identifier':
                    result = self.right.calc()
                    id_value_dict[self.left.value] = result
                    return f'{self.left.value} = {result}'
                else:
                    raise SyntaxError("Expected identifier before '='!") 

    
class Number(Node):
    def __init__(self, value):
        self.value = value


    def __repr__(self):
        return f'{self.value}'
    

    def calc(self):
        return self.value


class Identifier(Node):
    def __init__(self, value):
        self.value = value
    

    def __repr__(self):
        return f'{self.value}'
    

    def calc(self):
        if self.value in id_value_dict.keys():
            return id_value_dict[self.value]
        raise SyntaxError(f"Identifier '{self.value}' is not defined!")

    
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer


    def __factor(self) -> Node:
        self.lexer.next_token()
        match self.lexer.token.type:
            case "INT":
                value = int(self.lexer.token.value)
                self.lexer.next_token()
                return Number(value)
            case "FLOAT":
                value = float(self.lexer.token.value)
                self.lexer.next_token()
                return Number(value)
            case "ID":
                value = self.lexer.token.value
                self.lexer.next_token()
                return Identifier(value)
            case "LEFT_BR":
                value = self.equation()
                if self.lexer.token.type != 'RIGHT_BR':
                    raise SyntaxError('Left bracket is unpaired!')
                self.lexer.next_token()
                return value
            case "OPERATION":
                raise SyntaxError(f"Unexpected operation: '{self.lexer.token.value}'")
        return Number(0)


    def __term(self) -> Node:
        left = self.__factor()
        op = self.lexer.token.value
        while op in ('*', '/'):
            left = Operation_bin(op, left, self.__factor())
            op = self.lexer.token.value
        return left


    def __expression(self) -> Node:
        left = self.__term()
        op = self.lexer.token.value
        while op in ('+', '-'):
            left = Operation_bin(op, left, self.__term())
            op = self.lexer.token.value
        return left
    

    def equation(self) -> Node:
        left = self.__expression()
        op = self.lexer.token.value
        while op in ('=', '=='):
            left = Operation_bin(op, left, self.__expression())
            op = self.lexer.token.value
        return left
    

    def update_eq(self, eq):
        self.lexer = lex.Lexer(eq)

        
if __name__ == '__main__':
    parser = Parser(lex.Lexer(''))
    input_list = ['a=2.5*2', '3*(5+a)', '3*(5+a)==30/3+5*4']
    for input in input_list:
        parser.update_eq(input)
        print(parser.equation().calc())
