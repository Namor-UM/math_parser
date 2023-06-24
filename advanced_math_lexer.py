class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


    def __repr__(self):
        return f"{self.type} - {self.value}"
    

class Lexer:
    def __init__(self, source):
        self.source = source
        self.equal_sign_count = 0
        self.pos = 0
        self.token = Token(None, None)

    
    def next_token(self):
        if self.pos >= len(self.source):
            self.token = Token("EOF", "EOF")
            return self.token

        match self.source[self.pos]:
            case '(':
                self.pos += 1
                self.token = Token("LEFT_BR", self.source[self.pos - 1])
                return self.token
            case ')':
                self.pos += 1
                self.token = Token("RIGHT_BR", self.source[self.pos - 1])
                return self.token
            case '+' | '-' | '*' | '/' :
                self.pos += 1
                self.token = Token("OPERATOR", self.source[self.pos - 1])
                return self.token
            case '=':
                if self.equal_sign_count > 0:
                    raise SyntaxError(f'Only one equal-like sign allowed!')
                self.equal_sign_count += 1
                if self.pos + 1 < len(self.source):
                    if self.source[self.pos + 1] == '=':
                        self.pos += 2
                        self.token = Token("OPERATOR", '==')
                        return self.token
                
                self.pos += 1
                self.token = Token("OPERATOR", '=')
                return self.token

        next_pos = self.pos
        if self.source[self.pos].isnumeric():
            return_type = "INT"
            while next_pos < len(self.source) and self.source[next_pos] in "0123456789.":
                next_pos += 1
                if self.source[next_pos-1] == '.':
                    return_type = "FLOAT"

            if self.source[next_pos-1] == '.':
                raise SyntaxError(f'Unexpected symbol at {next_pos-1}: .')

            self.token =  Token(return_type, self.source[self.pos : next_pos])
            self.pos = next_pos
            return self.token

        elif self.source[self.pos].isalpha():
            while next_pos < len(self.source) and self.source[next_pos].isalnum():
                next_pos += 1
            
            self.token =  Token("ID", self.source[self.pos:next_pos])
            self.pos = next_pos
            return self.token
        
        raise SyntaxError(f"Unexpected symbol at {self.pos}: '{self.source[self.pos]}'")
        

if __name__ == '__main__':
    #lexer = Lexer("52.52/6*(5Alpha22)")
    lexer = Lexer("3*(5+a0)==20")

    while lexer.token.type != "EOF":
        if lexer.next_token() != None:
            print(lexer.token)