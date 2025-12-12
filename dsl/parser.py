from dsl.ast_nodes import PlusNode
from dsl.ast_nodes import MinusNode
from dsl.ast_nodes import TimesNode
from dsl.ast_nodes import DivideNode
from dsl.ast_nodes import ProgramNode
from dsl.ast_nodes import ReportNode
from dsl.ast_nodes import SaveNode
from dsl.ast_nodes import SetNode
from dsl.ast_nodes import IgniteNode
from dsl.ast_nodes import TeleportNode
from dsl.ast_nodes import SummonNode
from dsl.ast_nodes import MoveSummonsNode


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

            elif tok == "SET":
                self.consume("SET")
                amount = self.consume("NUMBER").value
                statements.append(SetNode(amount))
            
            elif tok == "TELEPORT":
                self.consume("TELEPORT")
                location = self.consume("IDENT").value
                statements.append(TeleportNode(location))
            
            elif tok == "IGNITE":
                self.consume("IGNITE")
                target_type = self.consume("IDENT").value
                target = self.consume("IDENT").value
                statements.append(IgniteNode(target_type, target))

            elif tok == "SUMMON":
                self.consume("SUMMON")
                entity = self.consume("IDENT").value
                statements.append(SummonNode(entity))
        
            elif tok == "MOVE":
                self.consume("MOVE")
                direction = self.consume("IDENT").value
                statements.append(MoveSummonsNode(direction))

            elif tok == "REPORT":
                self.consume("REPORT")
                statements.append(ReportNode())

            elif tok == "SAVE":
                self.consume("SAVE")
                statements.append(SaveNode())

            else:
                raise SyntaxError(f"Unexpected token: {tok}")

        return ProgramNode(statements)