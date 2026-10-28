import string
from dataclasses import dataclass
from typing import List, Optional

# ========== DELIMITERS & CHARACTER DEFINITIONS ==========
LETTERS = set(string.ascii_letters)
NONZERO = set("123456789")
NUMBERS = set("0123456789")
ASCII = set(string.printable)
INSC_ASCII = ASCII - {'"', "\\", "\n", "\r"}
ID_CHAR = LETTERS | NUMBERS | {"_"}
NEWLINE = {"\n", "\r"}

MATH_OP = {"+", "-", "*", "/", "%"}
REL_OP = {"<", ">", "="}
AND_OR_OP = {"&", "|"}

SPACE_DEL = {" ", "\t", "\n", "\r", "#"}
PAREN_DEL = SPACE_DEL | {"(", "#"}
CURLY_DEL = SPACE_DEL | {"{", "#"}
TRANSFER_DEL = SPACE_DEL | {";", "#"}

OPEN_PAREN_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", ")", "~", "+", "-", "!",'"', "#"}
CLOSE_PAREN_DEL = MATH_OP | REL_OP | AND_OR_OP | SPACE_DEL | {")", "{", "}", "]", "!", ";", ",", ":", "#"}
OPEN_CURLY_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "{", "}", "~", "+", "-", "!", '"', "#"}
CLOSE_CURLY_DEL = LETTERS | SPACE_DEL | {"}", ";", ",", "#"}
OPEN_BRACKET_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "~", "+", "-", "#"}
CLOSE_BRACKET_DEL = MATH_OP | REL_OP | AND_OR_OP | SPACE_DEL | {")", "}", "[", "]", "!", ";", ",", ":", "#"}

NEG_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "+", "-", "#"}
MATH_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "~", "#"}
CREMENT_DEL = LETTERS | SPACE_DEL | {")", "]", ";", ",", "#"}

REL_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "~", "+", "-", "#"}
EQUALITY_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "~", "+", "-", "!", '"', "#"}

LOG_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "~", "+", "-", "!", "#"}
NOT_DEL = LETTERS | SPACE_DEL | {"(", "#"}

BASE_ASSIGN_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "{", "~", "+", "-", "!", '"', "#"}
ASSIGN_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "~", "+", "-", "#"}

TERMINATOR_DEL = LETTERS | NUMBERS | SPACE_DEL | {"}", "#"}
COMMA_DEL = LETTERS | NUMBERS | SPACE_DEL | {"(", "{", "~", "+", "-", "!", '"', "#"}
CONCAT_DEL = LETTERS | SPACE_DEL | {"(", '"', "#"}

ID_DEL = MATH_OP | REL_OP | AND_OR_OP | SPACE_DEL | {"(", ")", "{", "}", "[", "]", "!", ".", ";", ",", ":", "#"}
AETHER_LIT_DEL = MATH_OP | REL_OP | AND_OR_OP | SPACE_DEL | {")", "{", "}", "]", "!", ";", ",", "#"}
ESSENCE_LIT_DEL = MATH_OP | REL_OP | AND_OR_OP | SPACE_DEL | {")", "}", "!", ";", ",", "#"}
INSCRIPTION_LIT_DEL = AND_OR_OP | SPACE_DEL | {")", "{", "}", "=", "!", ";", ",", ":", "#"}
AURA_LIT_DEL = AND_OR_OP | SPACE_DEL | {")", "}", "=", "!", ";", ",", "#"}

COMMENT_DEL = LETTERS | NUMBERS | SPACE_DEL | MATH_OP | REL_OP | AND_OR_OP | {"(", ")", "{", "}", "[", "]", "~", "!", ".", ";", ",", ":", '"', "#"}


# Characters that can begin a token (used to resynchronize after an error)
TOKEN_START = LETTERS | NUMBERS | MATH_OP | REL_OP | AND_OR_OP | {"~", "!", "(", ")", "{", "}", "[", "]", '"', ".", ";", ",", ":", "#"}

# ========== TOKEN STRUCTURE & CURSOR NAVIGATION ==========


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type:<18}, {repr(self.value):<15}, Line: {self.line:<2}, Col: {self.column:<2})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int, skip_number: bool = False):
        super().__init__(f"Lexical Error [Line {line}, Col {column}: {message}]")
        self.message = message
        self.line = line
        self.column = column
        self.skip_number = (
            skip_number  # recovery hint: skip the rest of a malformed number
        )


class Lexer:
    def __init__(self, source_code: str):
        self.source: str = source_code
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1
        self.tokens: List[Token] = []
        self.errors: List[LexerError] = []

    def current(self) -> Optional[str]:
        """Returns the character under the cursor without consuming it."""
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self) -> Optional[str]:
        """Returns the 1-character lookahead without consuming it."""
        next_pos = self.pos + 1
        return self.source[next_pos] if next_pos < len(self.source) else None

    def advance(self) -> str:
        """Consumes the current character and updates coordinate tracking."""
        ch = self.current()
        if ch is not None:
            self.pos += 1
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            return ch
        return ""

    # ========== RESERVED WORDS SCANNER (KEYWORDS, IDENTIFIERS) ==========
    def scan_word(self) -> Token:
        state = 0
        start_col = self.col
        lexeme = ""

        while True:
            ch = self.current()

            # ROOT STATE 0
            if state == 0:
                if ch == "a":
                    lexeme += self.advance()
                    state = 1
                elif ch == "b":
                    lexeme += self.advance()
                    state = 18
                elif ch == "c":
                    lexeme += self.advance()
                    state = 26
                elif ch == "d":
                    lexeme += self.advance()
                    state = 68
                elif ch == "e":
                    lexeme += self.advance()
                    state = 77
                elif ch == "f":
                    lexeme += self.advance()
                    state = 85
                elif ch == "g":
                    lexeme += self.advance()
                    state = 94
                elif ch == "i":
                    lexeme += self.advance()
                    state = 103
                elif ch == "m":
                    lexeme += self.advance()
                    state = 120
                elif ch == "p":
                    lexeme += self.advance()
                    state = 129
                elif ch == "r":
                    lexeme += self.advance()
                    state = 137
                elif ch == "s":
                    lexeme += self.advance()
                    state = 152
                elif ch == "y":
                    lexeme += self.advance()
                    state = 183
                elif ch in LETTERS:
                    lexeme += self.advance()
                    state = 257
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}'", self.line, start_col
                    )

            # AETHER (2-7), AURA (8-11)
            elif state == 1:
                if ch == "e":
                    lexeme += self.advance()
                    state = 2
                elif ch == "t":
                    lexeme += self.advance()
                    state = 8
                elif ch == "u":
                    lexeme += self.advance()
                    state = 14
                else:
                    state = 257

            # aether (2 -> 6)
            elif state == 2:
                if ch == "t":
                    lexeme += self.advance()
                    state = 3
                else:
                    state = 259
            elif state == 3:
                if ch == "h":
                    lexeme += self.advance()
                    state = 4
                else:
                    state = 261
            elif state == 4:
                if ch == "e":
                    lexeme += self.advance()
                    state = 5
                else:
                    state = 263
            elif state == 5:
                if ch == "r":
                    lexeme += self.advance()
                    state = 6
                else:
                    state = 265
            elif state == 6:
                if ch is None or ch in SPACE_DEL:
                    state = 7
                    return Token("aether", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            elif state == 8:
                if ch == "t":
                    lexeme += self.advance()
                    state = 9
                else:
                    state = 259
            elif state == 9:
                if ch == "u":
                    lexeme += self.advance()
                    state = 10
                else:
                    state = 261
            elif state == 10:
                if ch == "n":
                    lexeme += self.advance()
                    state = 11
                else:
                    state = 263
            elif state == 11:
                if ch == "e":
                    lexeme += self.advance()
                    state = 12
                else:
                    state = 265
            elif state == 12:
                if ch is None or ch in PAREN_DEL:
                    state = 13
                    return Token("attune", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # aura (8 -> 10)
            elif state == 14:
                if ch == "r":
                    lexeme += self.advance()
                    state = 15
                else:
                    state = 259
            elif state == 15:
                if ch == "a":
                    lexeme += self.advance()
                    state = 16
                else:
                    state = 261
            elif state == 16:
                if ch is None or ch in SPACE_DEL:
                    state = 17
                    return Token("aura", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 263
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # blessed (12-18)
            elif state == 18:
                if ch == "l":
                    lexeme += self.advance()
                    state = 19
                else:
                    state = 257
            elif state == 19:
                if ch == "e":
                    lexeme += self.advance()
                    state = 20
                else:
                    state = 259
            elif state == 20:
                if ch == "s":
                    lexeme += self.advance()
                    state = 21
                else:
                    state = 261
            elif state == 21:
                if ch == "s":
                    lexeme += self.advance()
                    state = 22
                else:
                    state = 263
            elif state == 22:
                if ch == "e":
                    lexeme += self.advance()
                    state = 23
                else:
                    state = 265
            elif state == 23:
                if ch == "d":
                    lexeme += self.advance()
                    state = 24
                else:
                    state = 267
            elif state == 24:
                if ch is None or ch in AURA_LIT_DEL:
                    state = 25
                    return Token("blessed", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 269
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # CAST (21-24), CHANT (25-29), CHARGE (30-33), CIRCLE (34-39), CONJURE (40-46), COUNTER (47-52), CROSSROAD (53-61), CURSED (62-67)
            elif state == 26:
                if ch == "a":
                    lexeme += self.advance()
                    state = 27
                elif ch == "h":
                    lexeme += self.advance()
                    state = 31
                elif ch == "i":
                    lexeme += self.advance()
                    state = 40
                elif ch == "o":
                    lexeme += self.advance()
                    state = 46
                elif ch == "r":
                    lexeme += self.advance()
                    state = 53
                elif ch == "u":
                    lexeme += self.advance()
                    state = 62
                else:
                    state = 257

            # cast (21-23)
            elif state == 27:
                if ch == "s":
                    lexeme += self.advance()
                    state = 28
                else:
                    state = 259
            elif state == 28:
                if ch == "t":
                    lexeme += self.advance()
                    state = 29
                else:
                    state = 261
            elif state == 29:
                if ch is None or ch in PAREN_DEL:
                    state = 30
                    return Token("cast", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 263
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # chant (25-28)
            elif state == 31:
                if ch == "a":
                    lexeme += self.advance()
                    state = 32
                else:
                    state = 259
            elif state == 32:
                if ch == "n":
                    lexeme += self.advance()
                    state = 33
                elif ch == "r":
                    lexeme += self.advance()
                    state = 36
                else:
                    state = 261
            elif state == 33:
                if ch == "t":
                    lexeme += self.advance()
                    state = 34
                else:
                    state = 263
            elif state == 34:
                if ch is None or ch in PAREN_DEL:
                    state = 35
                    return Token("chant", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 265
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # charge (30-32)
            elif state == 36:
                if ch == "g":
                    lexeme += self.advance()
                    state = 37
                else:
                    state = 263
            elif state == 37:
                if ch == "e":
                    lexeme += self.advance()
                    state = 38
                else:
                    state = 265
            elif state == 38:
                if ch is None or ch in PAREN_DEL:
                    state = 39
                    return Token("charge", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # circle (34-38)
            elif state == 40:
                if ch == "r":
                    lexeme += self.advance()
                    state = 41
                else:
                    state = 259
            elif state == 41:
                if ch == "c":
                    lexeme += self.advance()
                    state = 42
                else:
                    state = 261
            elif state == 42:
                if ch == "l":
                    lexeme += self.advance()
                    state = 43
                else:
                    state = 263
            elif state == 43:
                if ch == "e":
                    lexeme += self.advance()
                    state = 44
                else:
                    state = 265
            elif state == 44:
                if ch is None or ch in SPACE_DEL:
                    state = 45
                    return Token("circle", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # counter (47-51)
            elif state == 46:
                if ch == "u":
                    lexeme += self.advance()
                    state = 47
                else:
                    state = 259
            elif state == 47:
                if ch == "n":
                    lexeme += self.advance()
                    state = 48
                else:
                    state = 261
            elif state == 48:
                if ch == "t":
                    lexeme += self.advance()
                    state = 49
                else:
                    state = 263
            elif state == 49:
                if ch == "e":
                    lexeme += self.advance()
                    state = 50
                else:
                    state = 265
            elif state == 50:
                if ch == "r":
                    lexeme += self.advance()
                    state = 51
                else:
                    state = 267
            elif state == 51:
                if ch is None or ch in CURLY_DEL:
                    state = 52
                    return Token("counter", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 269
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # crossroad (53-60)
            elif state == 53:
                if ch == "o":
                    lexeme += self.advance()
                    state = 54
                else:
                    state = 259
            elif state == 54:
                if ch == "s":
                    lexeme += self.advance()
                    state = 55
                else:
                    state = 261
            elif state == 55:
                if ch == "s":
                    lexeme += self.advance()
                    state = 56
                else:
                    state = 263
            elif state == 56:
                if ch == "r":
                    lexeme += self.advance()
                    state = 57
                else:
                    state = 265
            elif state == 57:
                if ch == "o":
                    lexeme += self.advance()
                    state = 58
                else:
                    state = 267
            elif state == 58:
                if ch == "a":
                    lexeme += self.advance()
                    state = 59
                else:
                    state = 269
            elif state == 59:
                if ch == "d":
                    lexeme += self.advance()
                    state = 60
                else:
                    state = 271
            elif state == 60:
                if ch is None or ch in PAREN_DEL:
                    state = 61
                    return Token("crossroad", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 273
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # cursed (62-66)
            elif state == 62:
                if ch == "r":
                    lexeme += self.advance()
                    state = 63
                else:
                    state = 259
            elif state == 63:
                if ch == "s":
                    lexeme += self.advance()
                    state = 64
                else:
                    state = 261
            elif state == 64:
                if ch == "e":
                    lexeme += self.advance()
                    state = 65
                else:
                    state = 263
            elif state == 65:
                if ch == "d":
                    lexeme += self.advance()
                    state = 66
                else:
                    state = 265
            elif state == 66:
                if ch is None or ch in AURA_LIT_DEL:
                    state = 67
                    return Token("cursed", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # darkness (68-76)
            elif state == 68:
                if ch == "a":
                    lexeme += self.advance()
                    state = 69
                else:
                    state = 257
            elif state == 69:
                if ch == "r":
                    lexeme += self.advance()
                    state = 70
                else:
                    state = 259
            elif state == 70:
                if ch == "k":
                    lexeme += self.advance()
                    state = 71
                else:
                    state = 261
            elif state == 71:
                if ch == "n":
                    lexeme += self.advance()
                    state = 72
                else:
                    state = 263
            elif state == 72:
                if ch == "e":
                    lexeme += self.advance()
                    state = 73
                else:
                    state = 265
            elif state == 73:
                if ch == "s":
                    lexeme += self.advance()
                    state = 74
                else:
                    state = 267
            elif state == 74:
                if ch == "s":
                    lexeme += self.advance()
                    state = 75
                else:
                    state = 269
            elif state == 75:
                if ch is None or ch in SPACE_DEL:
                    state = 76
                    return Token("darkness", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 271
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # essence (77-76)
            elif state == 77:
                if ch == "s":
                    lexeme += self.advance()
                    state = 78
                else:
                    state = 257
            elif state == 78:
                if ch == "s":
                    lexeme += self.advance()
                    state = 79
                else:
                    state = 259
            elif state == 79:
                if ch == "e":
                    lexeme += self.advance()
                    state = 80
                else:
                    state = 261
            elif state == 80:
                if ch == "n":
                    lexeme += self.advance()
                    state = 81
                else:
                    state = 263
            elif state == 81:
                if ch == "c":
                    lexeme += self.advance()
                    state = 82
                else:
                    state = 265
            elif state == 82:
                if ch == "e":
                    lexeme += self.advance()
                    state = 83
                else:
                    state = 267
            elif state == 83:
                if ch is None or ch in SPACE_DEL:
                    state = 84
                    return Token("essence", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 269
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # fallback (85-93)
            elif state == 85:
                if ch == "a":
                    lexeme += self.advance()
                    state = 86
                else:
                    state = 257
            elif state == 86:
                if ch == "l":
                    lexeme += self.advance()
                    state = 87
                else:
                    state = 259
            elif state == 87:
                if ch == "l":
                    lexeme += self.advance()
                    state = 88
                else:
                    state = 261
            elif state == 88:
                if ch == "b":
                    lexeme += self.advance()
                    state = 89
                else:
                    state = 263
            elif state == 89:
                if ch == "a":
                    lexeme += self.advance()
                    state = 90
                else:
                    state = 265
            elif state == 90:
                if ch == "c":
                    lexeme += self.advance()
                    state = 91
                else:
                    state = 267
            elif state == 91:
                if ch == "k":
                    lexeme += self.advance()
                    state = 92
                else:
                    state = 269
            elif state == 92:
                if ch is None or ch in CURLY_DEL:
                    state = 93
                    return Token("fallback", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 271
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # grimoire (94-102)
            elif state == 94:
                if ch == "r":
                    lexeme += self.advance()
                    state = 95
                else:
                    state = 257
            elif state == 95:
                if ch == "i":
                    lexeme += self.advance()
                    state = 96
                else:
                    state = 259
            elif state == 96:
                if ch == "m":
                    lexeme += self.advance()
                    state = 97
                else:
                    state = 261
            elif state == 97:
                if ch == "o":
                    lexeme += self.advance()
                    state = 98
                else:
                    state = 263
            elif state == 98:
                if ch == "i":
                    lexeme += self.advance()
                    state = 99
                else:
                    state = 265
            elif state == 99:
                if ch == "r":
                    lexeme += self.advance()
                    state = 100
                else:
                    state = 267
            elif state == 100:
                if ch == "e":
                    lexeme += self.advance()
                    state = 101
                else:
                    state = 269
            elif state == 101:
                if ch is None or ch in PAREN_DEL:
                    state = 102
                    return Token("grimoire", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 271
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # INSCRIPTION (103-114), INVOKE (115-119)
            # inscription (103 - 113)
            elif state == 103:
                if ch == "n":
                    lexeme += self.advance()
                    state = 104
                else:
                    state = 257
            elif state == 104:
                if ch == "s":
                    lexeme += self.advance()
                    state = 105
                elif ch == "v":
                    lexeme += self.advance()
                    state = 115
                else:
                    state = 259
            elif state == 105:
                if ch == "c":
                    lexeme += self.advance()
                    state = 106
                else:
                    state = 261
            elif state == 106:
                if ch == "r":
                    lexeme += self.advance()
                    state = 107
                else:
                    state = 263
            elif state == 107:
                if ch == "i":
                    lexeme += self.advance()
                    state = 108
                else:
                    state = 265
            elif state == 108:
                if ch == "p":
                    lexeme += self.advance()
                    state = 109
                else:
                    state = 267
            elif state == 109:
                if ch == "t":
                    lexeme += self.advance()
                    state = 110
                else:
                    state = 269
            elif state == 110:
                if ch == "i":
                    lexeme += self.advance()
                    state = 111
                else:
                    state = 271
            elif state == 111:
                if ch == "o":
                    lexeme += self.advance()
                    state = 112
                else:
                    state = 273
            elif state == 112:
                if ch == "n":
                    lexeme += self.advance()
                    state = 113
                else:
                    state = 275
            elif state == 113:
                if ch is None or ch in SPACE_DEL:
                    state = 114
                    return Token("inscription", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 277
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # invoke (115-118)
            elif state == 115:
                if ch == "o":
                    lexeme += self.advance()
                    state = 116
                else:
                    state = 261
            elif state == 116:
                if ch == "k":
                    lexeme += self.advance()
                    state = 117
                else:
                    state = 263
            elif state == 117:
                if ch == "e":
                    lexeme += self.advance()
                    state = 118
                else:
                    state = 265
            elif state == 118:
                if ch is None or ch in CURLY_DEL:
                    state = 119
                    return Token("invoke", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # manifest (200-208)
            elif state == 120:
                if ch == "a":
                    lexeme += self.advance()
                    state = 121
                else:
                    state = 257
            elif state == 121:
                if ch == "n":
                    lexeme += self.advance()
                    state = 122
                else:
                    state = 259
            elif state == 122:
                if ch == "i":
                    lexeme += self.advance()
                    state = 123
                else:
                    state = 261
            elif state == 123:
                if ch == "f":
                    lexeme += self.advance()
                    state = 124
                else:
                    state = 263
            elif state == 124:
                if ch == "e":
                    lexeme += self.advance()
                    state = 125
                else:
                    state = 265
            elif state == 125:
                if ch == "s":
                    lexeme += self.advance()
                    state = 126
                else:
                    state = 267
            elif state == 126:
                if ch == "t":
                    lexeme += self.advance()
                    state = 127
                else:
                    state = 269
            elif state == 127:
                if ch is None or ch in PAREN_DEL:
                    state = 128
                    return Token("manifest", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 271
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # persist (214-221)
            elif state == 129:
                if ch == "e":
                    lexeme += self.advance()
                    state = 130
                else:
                    state = 257
            elif state == 130:
                if ch == "r":
                    lexeme += self.advance()
                    state = 131
                else:
                    state = 259
            elif state == 131:
                if ch == "s":
                    lexeme += self.advance()
                    state = 132
                else:
                    state = 261
            elif state == 132:
                if ch == "i":
                    lexeme += self.advance()
                    state = 133
                else:
                    state = 263
            elif state == 133:
                if ch == "s":
                    lexeme += self.advance()
                    state = 134
                else:
                    state = 265
            elif state == 134:
                if ch == "t":
                    lexeme += self.advance()
                    state = 135
                else:
                    state = 267
            elif state == 135:
                if ch is None or ch in TRANSFER_DEL:
                    state = 136
                    return Token("persist", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 269
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # RUNE (142-146), REMANIFEST (147-156)
            elif state == 137:
                if ch == "u":
                    lexeme += self.advance()
                    state = 138
                elif ch == "e":
                    lexeme += self.advance()
                    state = 142
                else:
                    state = 257

            # rune (142-145)
            elif state == 138:
                if ch == "n":
                    lexeme += self.advance()
                    state = 139
                else:
                    state = 259
            elif state == 139:
                if ch == "e":
                    lexeme += self.advance()
                    state = 140
                else:
                    state = 261
            elif state == 140:
                if ch is None or ch in SPACE_DEL:
                    state = 141
                    return Token("rune", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 263
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # remanifest (147-155)
            elif state == 142:
                if ch == "m":
                    lexeme += self.advance()
                    state = 143
                else:
                    state = 259
            elif state == 143:
                if ch == "a":
                    lexeme += self.advance()
                    state = 144
                else:
                    state = 261
            elif state == 144:
                if ch == "n":
                    lexeme += self.advance()
                    state = 145
                else:
                    state = 263
            elif state == 145:
                if ch == "i":
                    lexeme += self.advance()
                    state = 146
                else:
                    state = 265
            elif state == 146:
                if ch == "f":
                    lexeme += self.advance()
                    state = 147
                else:
                    state = 267
            elif state == 147:
                if ch == "e":
                    lexeme += self.advance()
                    state = 148
                else:
                    state = 269
            elif state == 148:
                if ch == "s":
                    lexeme += self.advance()
                    state = 149
                else:
                    state = 271
            elif state == 149:
                if ch == "t":
                    lexeme += self.advance()
                    state = 150
                else:
                    state = 273
            elif state == 150:
                if ch is None or ch in PAREN_DEL:
                    state = 151
                    return Token("remanifest", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 275
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # SCROLL (157-163), SEALED (164-169), SHATTER (170-176), SPELL (177-181), SUMMON (182-187)
            elif state == 152:
                if ch == "c":
                    lexeme += self.advance()
                    state = 153
                elif ch == "e":
                    lexeme += self.advance()
                    state = 159
                elif ch == "h":
                    lexeme += self.advance()
                    state = 165
                elif ch == "p":
                    lexeme += self.advance()
                    state = 172
                elif ch == "u":
                    lexeme += self.advance()
                    state = 177
                else:
                    state = 257

            # scroll (158-162)
            elif state == 153:
                if ch == "r":
                    lexeme += self.advance()
                    state = 154
                else:
                    state = 259
            elif state == 154:
                if ch == "o":
                    lexeme += self.advance()
                    state = 155
                else:
                    state = 261
            elif state == 155:
                if ch == "l":
                    lexeme += self.advance()
                    state = 156
                else:
                    state = 263
            elif state == 156:
                if ch == "l":
                    lexeme += self.advance()
                    state = 157
                else:
                    state = 265
            elif state == 157:
                if ch is None or ch in PAREN_DEL:
                    state = 158
                    return Token("scroll", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # sealed (164-168)
            elif state == 159:
                if ch == "a":
                    lexeme += self.advance()
                    state = 160
                else:
                    state = 259
            elif state == 160:
                if ch == "l":
                    lexeme += self.advance()
                    state = 161
                else:
                    state = 261
            elif state == 161:
                if ch == "e":
                    lexeme += self.advance()
                    state = 162
                else:
                    state = 263
            elif state == 162:
                if ch == "d":
                    lexeme += self.advance()
                    state = 163
                else:
                    state = 265
            elif state == 163:
                if ch is None or ch in SPACE_DEL:
                    state = 164
                    return Token("sealed", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # shatter (170-175)
            elif state == 165:
                if ch == "a":
                    lexeme += self.advance()
                    state = 166
                else:
                    state = 259
            elif state == 166:
                if ch == "t":
                    lexeme += self.advance()
                    state = 167
                else:
                    state = 261
            elif state == 167:
                if ch == "t":
                    lexeme += self.advance()
                    state = 168
                else:
                    state = 263
            elif state == 168:
                if ch == "e":
                    lexeme += self.advance()
                    state = 169
                else:
                    state = 265
            elif state == 169:
                if ch == "r":
                    lexeme += self.advance()
                    state = 170
                else:
                    state = 267
            elif state == 170:
                if ch is None or ch in TRANSFER_DEL:
                    state = 171
                    return Token("shatter", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 269
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # spell (177-180)
            elif state == 172:
                if ch == "e":
                    lexeme += self.advance()
                    state = 173
                else:
                    state = 259
            elif state == 173:
                if ch == "l":
                    lexeme += self.advance()
                    state = 174
                else:
                    state = 261
            elif state == 174:
                if ch == "l":
                    lexeme += self.advance()
                    state = 175
                else:
                    state = 263
            elif state == 175:
                if ch is None or ch in SPACE_DEL:
                    state = 176
                    return Token("spell", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 265
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # summon (182-186)
            elif state == 177:
                if ch == "m":
                    lexeme += self.advance()
                    state = 178
                else:
                    state = 259
            elif state == 178:
                if ch == "m":
                    lexeme += self.advance()
                    state = 179
                else:
                    state = 261
            elif state == 179:
                if ch == "o":
                    lexeme += self.advance()
                    state = 180
                else:
                    state = 263
            elif state == 180:
                if ch == "n":
                    lexeme += self.advance()
                    state = 181
                else:
                    state = 265
            elif state == 181:
                if ch is None or ch in SPACE_DEL:
                    state = 182
                    return Token("summon", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 267
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # yield (188-193)
            elif state == 183:
                if ch == "i":
                    lexeme += self.advance()
                    state = 184
                else:
                    state = 257
            elif state == 184:
                if ch == "e":
                    lexeme += self.advance()
                    state = 185
                else:
                    state = 259
            elif state == 185:
                if ch == "l":
                    lexeme += self.advance()
                    state = 186
                else:
                    state = 261
            elif state == 186:
                if ch == "d":
                    lexeme += self.advance()
                    state = 187
                else:
                    state = 263
            elif state == 187:
                if ch is None or ch in TRANSFER_DEL:
                    state = 188
                    return Token("yield", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 265
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # IDENTIFIER STATES: 257-287
            elif 257 <= state <= 287 and state % 2 == 1:
                if ch in ID_DEL or ch is None:
                    state = state + 1
                    return Token("id", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    if state == 287:
                        raise LexerError(
                            f"'{lexeme}' has invalid delimiter '{ch}'",
                            self.line,
                            self.col,
                        )
                    lexeme += self.advance()
                    state = state + 2
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after identifier '{lexeme}'",
                        self.line,
                        self.col,
                    )

    # ========== RESERVED SYMBOLS SCANNER ==========
    def scan_symbol(self) -> Token:
        state = 0
        start_col = self.col
        lexeme = ""

        while True:
            ch = self.current()

            if state == 0:
                if ch == "(":
                    lexeme += self.advance()
                    state = 189
                elif ch == ")":
                    lexeme += self.advance()
                    state = 191
                elif ch == "{":
                    lexeme += self.advance()
                    state = 193
                elif ch == "}":
                    lexeme += self.advance()
                    state = 195
                elif ch == "[":
                    lexeme += self.advance()
                    state = 197
                elif ch == "]":
                    lexeme += self.advance()
                    state = 199
                elif ch == "~":
                    lexeme += self.advance()
                    state = 201
                elif ch == "+":
                    lexeme += self.advance()
                    state = 203
                elif ch == "-":
                    lexeme += self.advance()
                    state = 209
                elif ch == "*":
                    lexeme += self.advance()
                    state = 215
                elif ch == "/":
                    lexeme += self.advance()
                    state = 219
                elif ch == "%":
                    lexeme += self.advance()
                    state = 223
                elif ch == ">":
                    lexeme += self.advance()
                    state = 227
                elif ch == "<":
                    lexeme += self.advance()
                    state = 231
                elif ch == "=":
                    lexeme += self.advance()
                    state = 235
                elif ch == "!":
                    lexeme += self.advance()
                    state = 239
                elif ch == "&":
                    lexeme += self.advance()
                    state = 243
                elif ch == "|":
                    lexeme += self.advance()
                    state = 246
                elif ch == ".":
                    lexeme += self.advance()
                    state = 249
                elif ch == ";":
                    lexeme += self.advance()
                    state = 251
                elif ch == ",":
                    lexeme += self.advance()
                    state = 253
                elif ch == ":":
                    lexeme += self.advance()
                    state = 255
                else:
                    raise LexerError(
                        f"Unexpected symbol character '{ch}'", self.line, start_col
                    )

            # '(' (196 -> 197*)
            elif state == 189:
                if ch is None or ch in OPEN_PAREN_DEL:
                    state = 190
                    return Token("(", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '('", self.line, self.col
                )

            # ')' (194 -> 195*)
            elif state == 191:
                if ch in CLOSE_PAREN_DEL:
                    state = 192
                    return Token(")", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ')'", self.line, self.col
                )

            # '{' (200 -> 201*)
            elif state == 193:
                if ch is None or ch in OPEN_CURLY_DEL:
                    state = 194
                    return Token("{", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '{{'", self.line, self.col
                )

            # '}' (198 -> 199*)
            elif state == 195:
                if ch in CLOSE_CURLY_DEL:
                    state = 196
                    return Token("}", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '}}'", self.line, self.col
                )

            # '[' (202 -> 203*)
            elif state == 197:
                if ch in OPEN_BRACKET_DEL:
                    state = 198
                    return Token("[", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '['", self.line, self.col
                )

            # ']' (204 -> 205*)
            elif state == 199:
                if ch is None or ch in CLOSE_BRACKET_DEL:
                    state = 200
                    return Token("]", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ']'", self.line, self.col
                )

            # '~' (206 -> 207*)
            elif state == 201:
                if ch in NEG_DEL:
                    state = 202
                    return Token("~", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '~'", self.line, self.col
                )

            # '+' branch (208 -> 213*)
            elif state == 203:
                if ch == "+":
                    lexeme += self.advance()
                    state = 205
                elif ch == "=":
                    lexeme += self.advance()
                    state = 207
                elif ch in MATH_DEL:
                    state = 204
                    return Token("+", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '+'", self.line, self.col
                    )

            # '++' (210 -> 211*)
            elif state == 205:
                if ch is None or ch in CREMENT_DEL:
                    state = 206
                    return Token("++", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '++'", self.line, self.col
                )

            # '+=' (212 -> 213*)
            elif state == 207:
                if ch in ASSIGN_DEL:
                    state = 208
                    return Token("+=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '+='", self.line, self.col
                )

            # '-' branch (214 -> 219*)
            elif state == 209:
                if ch == "-":
                    lexeme += self.advance()
                    state = 211
                elif ch == "=":
                    lexeme += self.advance()
                    state = 213
                elif ch in MATH_DEL:
                    state = 210
                    return Token("-", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '-'", self.line, self.col
                    )

            # '--' (216 -> 217*)
            elif state == 211:
                if ch is None or ch in CREMENT_DEL:
                    state = 212
                    return Token("--", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '--'", self.line, self.col
                )

            # '-=' (218 -> 219*)
            elif state == 213:
                if ch in ASSIGN_DEL:
                    state = 214
                    return Token("-=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '-='", self.line, self.col
                )

            # '*' branch (220 -> 223*)
            elif state == 215:
                if ch == "=":
                    lexeme += self.advance()
                    state = 217
                elif ch in MATH_DEL:
                    state = 216
                    return Token("*", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '*'", self.line, self.col
                    )

            # '*=' (222 -> 223*)
            elif state == 217:
                if ch in ASSIGN_DEL:
                    state = 218
                    return Token("*=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '*='", self.line, self.col
                )

            # '/' branch (224 -> 227*)
            elif state == 219:
                if ch == "=":
                    lexeme += self.advance()
                    state = 221
                elif ch in MATH_DEL:
                    state = 220
                    return Token("/", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '/'", self.line, self.col
                    )

            # '/=' (226 -> 227*)
            elif state == 221:
                if ch in ASSIGN_DEL:
                    state = 222
                    return Token("/=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '/='", self.line, self.col
                )

            # '%' branch (228 -> 231*)
            elif state == 223:
                if ch == "=":
                    lexeme += self.advance()
                    state = 225
                elif ch in MATH_DEL:
                    state = 224
                    return Token("%", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '%'", self.line, self.col
                    )

            # '%=' (230 -> 231*)
            elif state == 225:
                if ch in ASSIGN_DEL:
                    state = 226
                    return Token("%=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '%='", self.line, self.col
                )

            # '>' branch (232 -> 235*)
            elif state == 227:
                if ch == "=":
                    lexeme += self.advance()
                    state = 229
                elif ch in REL_DEL:
                    state = 228
                    return Token(">", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '>'", self.line, self.col
                    )

            # '>=' (234 -> 235*)
            elif state == 229:
                if ch in REL_DEL:
                    state = 230
                    return Token(">=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '>='", self.line, self.col
                )

            # '<' branch (236 -> 239*)
            elif state == 231:
                if ch == "=":
                    lexeme += self.advance()
                    state = 233
                elif ch in REL_DEL:
                    state = 232
                    return Token("<", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '<'", self.line, self.col
                    )

            # '<=' (238 -> 239*)
            elif state == 233:
                if ch in REL_DEL:
                    state = 234
                    return Token("<=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '<='", self.line, self.col
                )

            # '=' branch (240 -> 243*)
            elif state == 235:
                if ch == "=":
                    lexeme += self.advance()
                    state = 237
                elif ch in BASE_ASSIGN_DEL:
                    state = 236
                    return Token("=", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '='", self.line, self.col
                    )

            # '==' (242 -> 243*)
            elif state == 237:
                if ch in EQUALITY_DEL:
                    state = 238
                    return Token("==", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '=='", self.line, self.col
                )

            # '!' branch (244 -> 247*)
            elif state == 239:
                if ch == "=":
                    lexeme += self.advance()
                    state = 241
                elif ch in NOT_DEL:
                    state = 240
                    return Token("!", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '!'", self.line, self.col
                    )

            # '!=' (246 -> 247*)
            elif state == 241:
                if ch in EQUALITY_DEL:
                    state = 242
                    return Token("!=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '!='", self.line, self.col
                )

            # '&&' (248 -> 250*)
            elif state == 243:
                if ch == "&":
                    lexeme += self.advance()
                    state = 244
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' after '&'. Expected '&&'",
                        self.line,
                        self.col,
                    )

            elif state == 244:
                if ch in LOG_DEL:
                    state = 245
                    return Token("&&", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '&&'", self.line, self.col
                )

            # '||' (251 -> 253*)
            elif state == 246:
                if ch == "|":
                    lexeme += self.advance()
                    state = 247
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' after '|'. Expected '||'",
                        self.line,
                        self.col,
                    )

            elif state == 247:
                if ch in LOG_DEL:
                    state = 248
                    return Token("||", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '||'", self.line, self.col
                )

            # '.' (254 -> 255*)
            elif state == 249:
                if ch in LETTERS:
                    state = 250
                    return Token(".", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '.'", self.line, self.col
                )

            # ';' (256 -> 257*)
            elif state == 251:
                if ch is None or ch in TERMINATOR_DEL:
                    state = 252
                    return Token(";", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ';'", self.line, self.col
                )

            # ',' (258 -> 259*)
            elif state == 253:
                if ch in COMMA_DEL:
                    state = 254
                    return Token(",", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ','", self.line, self.col
                )

            # ':' (258 -> 259*)
            elif state == 255:
                if ch in CONCAT_DEL:
                    state = 256
                    return Token(":", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ':'", self.line, self.col
                )

    # ========== LITERALS SCANNER ==========
    def scan_number(self) -> Token:
        """Scans an aeth_lit or ess_lit. '~' is a separate token, so a literal never starts with it.

        State numbers follow the transition diagram:
            0            start
            289 / 290    '0'  /  accept aether '0'
            291 .. 321   odd states = 1..16 integer digits; the accept state is the state + 1
            323          just after '.'; the fraction is read here with a digit counter
                        (diagram states 323..349 describe the same language)
        """
        state = 0
        start_col = self.col
        lexeme = ""
        frac_len = 0

        while True:
            ch = self.current()

            # ROOT STATE 0: '0' -> 289, nonzero -> 291
            if state == 0:
                if ch == "0":
                    lexeme += self.advance()
                    state = 289
                elif ch is not None and ch in NONZERO:
                    lexeme += self.advance()
                    state = 291
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' in number",
                        self.line,
                        start_col,
                    )

            # '0' (289): '.' -> 323, aether_lit_del -> 290*
            elif state == 289:
                if ch == ".":
                    lexeme += self.advance()
                    state = 323
                elif ch is None or ch in AETHER_LIT_DEL:
                    state = 290
                    return Token("aeth_lit", lexeme, self.line, start_col)
                elif ch in NUMBERS:
                    raise LexerError(
                        f"Leading zeros are not allowed ('{lexeme}{ch}')",
                        self.line,
                        start_col,
                        skip_number=True,
                    )
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after aether literal '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # integer digits: 291 (1 digit), 293 (2), ... , 321 (16)
            #   numbers -> state + 2, '.' -> 323, aether_lit_del -> state + 1 (accept)
            elif 291 <= state <= 321 and state % 2 == 1:
                if ch is not None and ch in NUMBERS:
                    if state == 321:  # a 17th digit
                        raise LexerError(
                            f"'{lexeme}' has invalid delimiter '{ch}'",
                            self.line,
                            self.col,
                        )
                    lexeme += self.advance()
                    state += 2
                elif ch == ".":
                    lexeme += self.advance()
                    state = 323
                elif ch is None or ch in AETHER_LIT_DEL:
                    state += 1
                    return Token("aeth_lit", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after aether literal '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # after '.' (323): at least one fractional digit is required
            elif state == 323:
                if ch is not None and ch in NUMBERS:
                    lexeme += self.advance()
                    frac_len = 1
                    state = 326
                else:
                    raise LexerError(
                        f"Expected a digit after '.' in '{lexeme}'", self.line, self.col
                    )

            # fractional digits (diagram states 326..349), kept as one state with a counter:
            # the fraction is "0", or 1 to 7 digits followed by a nonzero digit (1..8 digits).
            # Any digit may be read (the 'numbers' edge); the literal may only END on a
            # nonzero digit (the 'nonzero' edge), except the lone ".0".
            elif state == 326:
                if ch is not None and ch in NUMBERS:
                    if frac_len == 8:  # a 9th fractional digit
                        raise LexerError(
                            f"'{lexeme}' has invalid delimiter '{ch}'",
                            self.line,
                            self.col,
                        )
                    lexeme += self.advance()
                    frac_len += 1
                elif ch is None or ch in ESSENCE_LIT_DEL:
                    frac = lexeme.split(".")[1]
                    if frac != "0" and frac[-1] == "0":
                        raise LexerError(
                            f"Essence literal '{lexeme}' cannot end in 0",
                            self.line,
                            start_col,
                        )
                    return Token("ess_lit", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after essence literal '{lexeme}'",
                        self.line,
                        self.col,
                    )

    def scan_string(self) -> Optional[Token]:
        """Scans an insc_lit. States follow the transition diagram:
        0 -'"'-> 350 (loop on insc_ascii) -'"'-> 351 -inscription_lit_del-> 352*
        """
        state = 0
        start_line = self.line
        start_col = self.col
        lexeme = ""
        bad = False  # an invalid character was found; the string is still read to its end

        while True:
            ch = self.current()

            if state == 0:
                if ch == '"':
                    lexeme += self.advance()
                    state = 350
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' (expected '\"')",
                        self.line,
                        start_col,
                    )

            # inside the string (350): insc_ascii loops, '"' closes it
            elif state == 350:
                if ch is None or ch in NEWLINE:
                    raise LexerError(
                        f"Unterminated inscription literal: {lexeme}",
                        start_line,
                        start_col,
                    )
                elif ch == '"':
                    lexeme += self.advance()
                    state = 351
                elif ch == "\\":
                    # The lexer does not check which escape it is: a backslash and the character
                    # after it are both kept in the lexeme (so \" does not end the string).
                    # NOTE: this edge is not drawn in the diagram yet (see the notes).
                    lexeme += self.advance()
                    esc = self.current()
                    if esc is None or esc in NEWLINE:
                        raise LexerError(
                            f"Unterminated inscription literal: {lexeme}",
                            start_line,
                            start_col,
                        )
                    if esc not in ASCII:
                        self.errors.append(
                            LexerError(
                                f"Invalid character '{esc}' in inscription literal",
                                self.line,
                                self.col,
                            )
                        )
                        bad = True
                    lexeme += self.advance()
                elif ch in INSC_ASCII:
                    lexeme += self.advance()
                else:
                    self.errors.append(
                        LexerError(
                            f"Invalid character '{ch}' in inscription literal",
                            self.line,
                            self.col,
                        )
                    )
                    bad = True
                    lexeme += self.advance()

            # after the closing quote (351): inscription_lit_del -> 352*
            elif state == 351:
                if ch is None or ch in INSCRIPTION_LIT_DEL:
                    state = 352
                    return (
                        None
                        if bad
                        else Token("insc_lit", lexeme, start_line, start_col)
                    )
                raise LexerError(
                    f"Invalid delimiter '{ch}' after inscription literal",
                    self.line,
                    self.col,
                )
    
    def scan_comment(self) -> Token:
        """Scans a comment. States follow the transition diagram:
        0 -'#'-> 353 -'/'-> 354 (loop on ascii) -'/'-> 355 -'#'-> 356 -space_del-> 357*
        """
        state = 0
        start_line = self.line
        start_col = self.col
        lexeme = ""

        while True:
            ch = self.current()

            if state == 0:
                if ch == "#":
                    lexeme += self.advance()
                    state = 353
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' (expected '#/')",
                        self.line,
                        start_col,
                    )

            # '#' read (353): the opener must be '#/'
            elif state == 353:
                if ch == "/":
                    lexeme += self.advance()
                    state = 354
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '#'", self.line, self.col
                    )

            # inside the comment (354): ascii loops, '/' may start the closer '/#'
            elif state == 354:
                if ch is None:
                    raise LexerError(
                        f"Unterminated comment: {lexeme}", start_line, start_col
                    )
                elif ch == "/":
                    lexeme += self.advance()
                    state = 355
                elif ch in ASCII:
                    lexeme += self.advance()
                else:
                    # report it, but stay inside the comment so the rest isn't tokenized as code
                    self.errors.append(
                        LexerError(
                            f"Invalid character '{ch}' in comment",
                            self.line,
                            self.col,
                        )
                    )
                    lexeme += self.advance()

            # '/' read inside the comment (355): '#' closes it, anything else goes back to 354
            elif state == 355:
                if ch == "#":
                    lexeme += self.advance()
                    state = 356
                else:
                    state = 354

            # closer '/#' read (356): space_del -> 357*
            elif state == 356:
                if ch is None or ch in COMMENT_DEL:
                    state = 357
                    return Token("comment", lexeme, start_line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after comment", self.line, self.col
                )
                
    def scan_whitespace(self) -> Token:
        start_line, start_col = self.line, self.col
        ch = self.current()
        if ch in {" ", "\t"}:
            return Token("whitespace", self.advance(), start_line, start_col)
        lexeme = self.advance()                      # "\n" or a lone "\r"
        if lexeme == "\r" and self.current() == "\n":
            lexeme += self.advance()
        return Token("newline", lexeme, start_line, start_col)

    # ========== TOKENIZER ==========
    def tokenize(self) -> List[Token]:
        """Scans the whole source. Lexical errors are collected in self.errors instead of stopping the scan."""
        while True:
            ch = self.current()
            if ch is None:
                break

            start_pos = self.pos
            try:
                if ch in LETTERS:
                    token = self.scan_word()
                elif ch in NUMBERS:
                    token = self.scan_number()
                elif ch in {'"'}:
                    token = self.scan_string()
                elif ch == "#" and self.peek() == "/":
                    token = self.scan_comment()
                elif ch in SPACE_DEL:
                    token = self.scan_whitespace()
                else:
                    token = self.scan_symbol()
            except LexerError as err:
                self.errors.append(err)
                self.recover(err, start_pos)
                continue

            if token is not None:
                self.tokens.append(token)

        return self.tokens

    def recover(self, err: LexerError, start_pos: int) -> None:
        """Moves the cursor to where scanning can safely resume after an error.

        Most errors leave the cursor ON the offending character, so scanning resumes there
        (e.g. 'abcdefghabcdefghij' -> error at 'i', then 'ij' is read as a new identifier).
        """
        if err.skip_number:
            while self.current() is not None and (
                self.current() in NUMBERS or self.current() == "."
            ):
                self.advance()
        ch = self.current()
        # always make progress; and drop an offending character that cannot start any token
        # (it was already reported), so one bad character doesn't produce two errors
        if self.pos == start_pos or (
            ch is not None and ch not in TOKEN_START and ch not in SPACE_DEL
        ):
            self.advance()


def tokenize(lexer: "Lexer") -> List[Token]:
    """Module-level entry point kept for app.py, which calls tokenize(lexer)."""
    return lexer.tokenize()
