from ast_nodes import PlusNode
from ast_nodes import MinusNode
from ast_nodes import TimesNode
from ast_nodes import DivideNode
from ast_nodes import ProgramNode
from ast_nodes import ReportNode
from ast_nodes import SaveNode
from ast_nodes import SetNode
from ast_nodes import UndoNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, type=None):
        tok = self.tokens[self.pos]
        if type and tok.type != type:
            raise SyntaxError(f"Expected {type}, got {tok.type}")
        self.pos += 1
        return tok

    def parse(self):
        statements = []

        while self.peek().type != "EOF":
            tok = self.peek().type

            if tok == "PLUS":
                self.consume("PLUS")
                amount = self.consume("NUMBER").value
                statements.append(PlusNode(amount))

            elif tok == "MINUS":
                self.consume("MINUS")
                amount = self.consume("NUMBER").value
                statements.append(MinusNode(amount))

            elif tok == "TIMES":
                self.consume("TIMES")
                amount = self.consume("NUMBER").value
                statements.append(TimesNode(amount))

            elif tok == "DIVIDE":
                self.consume("DIVIDE")
                amount = self.consume("NUMBER").value
                statements.append(DivideNode(amount))

            elif tok == "UNDO":
                self.consume("UNDO")
                statements.append(UndoNode())

            elif tok == "SET":
                self.consume("SET")
                amount = self.consume("NUMBER").value
                statements.append(SetNode(amount))

            elif tok == "REPORT":
                self.consume("REPORT")
                statements.append(ReportNode())

            elif tok == "SAVE":
                self.consume("SAVE")
                statements.append(SaveNode())

            else:
                raise SyntaxError(f"Unexpected token: {tok}")

        return ProgramNode(statements)