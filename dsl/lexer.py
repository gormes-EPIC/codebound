class Token:
    def __init__(self, type, value):
        self.type = type  # token type
        self.value = value  # the string or number
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    
def tokenize(text):
    words = text.split()
    tokens = []

    i = 0
    while i < len(words):
        w = words[i]

        if w.isdigit():
            tokens.append(Token("NUMBER", float(w)))
        elif w.lower() in ("report", "teleport", "ignite", "summon", "move", "draw", "remember", "alert"):
            tokens.append(Token(w.upper(), w))
        else:
            tokens.append(Token("IDENT", w))
        
        i += 1

    tokens.append(Token("EOF", "eof"))
    return tokens