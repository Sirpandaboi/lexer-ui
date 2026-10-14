import string
from dataclasses import dataclass
from typing import List, Optional

# ========== DELIMITERS & CHARACTER DEFINITIONS ==========

# CHARACTER SETS
LETTERS = set(string.ascii_letters)
NONZERO = set("123456789")
NUMBERS = set("0123456789")
ASCII = set(string.printable) - {"\x0b", "\x0c"}
INSC_ASCII = ASCII - {'"', "\\", "\n", "\r", "\x0b", "\x0c"}
ESCAPE_CHARS = {"n", "t", "r", "\\", '"'}
UNDERSCORE = {"_"}
ID_CHAR = LETTERS | NUMBERS | UNDERSCORE

# WHITESPACE & PUNCTUATION
WHITESPACE = {" ", "\t"}
NEWLINE = {"\n", "\r"}
TERMINATOR = {";"}
COMMA = {","}
DOT = {"."}

# OPERATORS
MATH_OP = {"+", "-", "*", "/", "%"}
NEG_OP = {"~"}
REL_OP = {"<", ">", "="}
EQUAL_OP = {"="}
AND_OR_OP = {"&", "|"}
NOT_OP = {"!"}

# GROUPINGS & QUOTES
OPEN_PAREN = {"("}
CLOSE_PAREN = {")"}
OPEN_CURLY = {"{"}
CLOSE_CURLY = {"}"}
OPEN_BRACKET = {"["}
CLOSE_BRACKET = {"]"}
OPEN_QUOTE = {'"'}
HASHTAG = {"#"}

# GENERAL DELIMITERS
SPACE_DEL = WHITESPACE | NEWLINE
PAREN_DEL = WHITESPACE | OPEN_PAREN
CURLY_DEL = OPEN_CURLY | SPACE_DEL
TRANSFER_DEL = WHITESPACE | TERMINATOR

# GROUPING DELIMITERS
OPEN_PAREN_DEL = (
    LETTERS | NUMBERS | NEG_OP | NOT_OP | CLOSE_PAREN | OPEN_QUOTE | PAREN_DEL
)
CLOSE_PAREN_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | AND_OR_OP
    | HASHTAG
    | CLOSE_PAREN
    | OPEN_CURLY
    | CLOSE_CURLY
    | CLOSE_BRACKET
    | SPACE_DEL
)
OPEN_CURLY_DEL = (
    LETTERS | NUMBERS | NEG_OP | HASHTAG | OPEN_CURLY | CLOSE_CURLY | OPEN_QUOTE | SPACE_DEL
)
CLOSE_CURLY_DEL = LETTERS | TERMINATOR | COMMA | HASHTAG | CLOSE_CURLY | SPACE_DEL
OPEN_BRACKET_DEL = LETTERS | NUMBERS | PAREN_DEL
CLOSE_BRACKET_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | EQUAL_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | OPEN_BRACKET
    | CLOSE_BRACKET
    | SPACE_DEL
)

# OPERATOR DELIMITERS
MATH_DEL = LETTERS | NUMBERS | NEG_OP | PAREN_DEL
CREMENT_DEL = (
    WHITESPACE | TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | CLOSE_BRACKET
)
REL_DEL = LETTERS | NUMBERS | WHITESPACE | NEG_OP | OPEN_PAREN
EQUALITY_DEL = REL_DEL | OPEN_QUOTE
LOG_DEL = REL_DEL | NOT_OP
NOT_DEL = LETTERS | PAREN_DEL
NEG_DEL = NUMBERS | LETTERS | OPEN_PAREN

ASSIGN_DEL = LETTERS | NUMBERS | WHITESPACE | NEG_OP | OPEN_PAREN
BASE_ASSIGN_DEL = NOT_OP | OPEN_CURLY | OPEN_QUOTE | ASSIGN_DEL

# PUNCTUATION DELIMITERS
TERMINATOR_DEL = HASHTAG | CLOSE_CURLY | SPACE_DEL
COMMA_DEL = (
    LETTERS | NUMBERS | NEG_OP | HASHTAG |OPEN_PAREN | OPEN_CURLY | OPEN_QUOTE | SPACE_DEL
)

# IDENTIFIER & LITERAL DELIMITERS
ID_DEL = (
    TERMINATOR
    | COMMA
    | DOT
    | MATH_OP
    | REL_OP
    | EQUAL_OP
    | AND_OR_OP
    | NOT_OP
    | OPEN_PAREN
    | CLOSE_PAREN
    | OPEN_CURLY
    | CLOSE_CURLY
    | OPEN_BRACKET
    | CLOSE_BRACKET
    | SPACE_DEL
)
AETHER_LIT_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | AND_OR_OP
    | NOT_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | CLOSE_BRACKET
    | SPACE_DEL
)
ESSENCE_LIT_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | AND_OR_OP
    | NOT_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | SPACE_DEL
)
INSCRIPTION_LIT_DEL = TERMINATOR | COMMA | EQUAL_OP | NOT_OP | CLOSE_PAREN | OPEN_CURLY | CLOSE_CURLY | SPACE_DEL
AURA_LIT_DEL = (
    TERMINATOR
    | COMMA
    | EQUAL_OP
    | AND_OR_OP
    | NOT_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | SPACE_DEL
)

# Characters that can begin a token (used to resynchronize after an error)
TOKEN_START = (
    LETTERS
    | NUMBERS
    | NEG_OP
    | REL_OP
    | AND_OR_OP
    | NOT_OP
    | OPEN_PAREN
    | CLOSE_PAREN
    | OPEN_CURLY
    | CLOSE_CURLY
    | OPEN_BRACKET
    | CLOSE_BRACKET
    | OPEN_QUOTE
    | DOT
    | TERMINATOR
    | COMMA
    | {"#"}
)

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
                    state = 12
                elif ch == "c":
                    lexeme += self.advance()
                    state = 20
                elif ch == "d":
                    lexeme += self.advance()
                    state = 62
                elif ch == "e":
                    lexeme += self.advance()
                    state = 71
                elif ch == "f":
                    lexeme += self.advance()
                    state = 79
                elif ch == "g":
                    lexeme += self.advance()
                    state = 88
                elif ch == "i":
                    lexeme += self.advance()
                    state = 97
                elif ch == "m":
                    lexeme += self.advance()
                    state = 114
                elif ch == "n":
                    lexeme += self.advance()
                    state = 123
                elif ch == "p":
                    lexeme += self.advance()
                    state = 128
                elif ch == "r":
                    lexeme += self.advance()
                    state = 136
                elif ch == "s":
                    lexeme += self.advance()
                    state = 151
                elif ch == "y":
                    lexeme += self.advance()
                    state = 182
                elif ch in LETTERS:
                    lexeme += self.advance()
                    state = 254
                else:
                    raise LexerError(
                        f"Unexpected character {repr(ch)}", self.line, start_col
                    )

            # AETHER (2-7), AURA (8-11)
            elif state == 1:
                if ch == "e":
                    lexeme += self.advance()
                    state = 2
                elif ch == "u":
                    lexeme += self.advance()
                    state = 8
                else:
                    state = 254

            # aether (2 -> 6)
            elif state == 2:
                if ch == "t":
                    lexeme += self.advance()
                    state = 3
                else:
                    state = 256
            elif state == 3:
                if ch == "h":
                    lexeme += self.advance()
                    state = 4
                else:
                    state = 258
            elif state == 4:
                if ch == "e":
                    lexeme += self.advance()
                    state = 5
                else:
                    state = 260
            elif state == 5:
                if ch == "r":
                    lexeme += self.advance()
                    state = 6
                else:
                    state = 262
            elif state == 6:
                if ch is None or ch in WHITESPACE:
                    state = 7
                    return Token("aether", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # aura (8 -> 10)
            elif state == 8:
                if ch == "r":
                    lexeme += self.advance()
                    state = 9
                else:
                    state = 256
            elif state == 9:
                if ch == "a":
                    lexeme += self.advance()
                    state = 10
                else:
                    state = 258
            elif state == 10:
                if ch is None or ch in WHITESPACE:
                    state = 11
                    return Token("aura", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 260
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # blessed (12-18)
            elif state == 12:
                if ch == "l":
                    lexeme += self.advance()
                    state = 13
                else:
                    state = 254
            elif state == 13:
                if ch == "e":
                    lexeme += self.advance()
                    state = 14
                else:
                    state = 256
            elif state == 14:
                if ch == "s":
                    lexeme += self.advance()
                    state = 15
                else:
                    state = 258
            elif state == 15:
                if ch == "s":
                    lexeme += self.advance()
                    state = 16
                else:
                    state = 260
            elif state == 16:
                if ch == "e":
                    lexeme += self.advance()
                    state = 17
                else:
                    state = 262
            elif state == 17:
                if ch == "d":
                    lexeme += self.advance()
                    state = 18
                else:
                    state = 264
            elif state == 18:
                if ch is None or ch in AURA_LIT_DEL:
                    state = 19
                    return Token("blessed", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 266
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # CAST (21-24), CHANT (25-29), CHARGE (30-33), CIRCLE (34-39), CONJURE (40-46), COUNTER (47-52), CROSSROAD (53-61), CURSED (62-67)
            elif state == 20:
                if ch == "a":
                    lexeme += self.advance()
                    state = 21
                elif ch == "h":
                    lexeme += self.advance()
                    state = 25
                elif ch == "i":
                    lexeme += self.advance()
                    state = 34
                elif ch == "o":
                    lexeme += self.advance()
                    state = 40
                elif ch == "r":
                    lexeme += self.advance()
                    state = 47
                elif ch == "u":
                    lexeme += self.advance()
                    state = 56
                else:
                    state = 254

            # cast (21-23)
            elif state == 21:
                if ch == "s":
                    lexeme += self.advance()
                    state = 22
                else:
                    state = 256
            elif state == 22:
                if ch == "t":
                    lexeme += self.advance()
                    state = 23
                else:
                    state = 258
            elif state == 23:
                if ch is None or ch in PAREN_DEL:
                    state = 24
                    return Token("cast", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 260
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # chant (25-28)
            elif state == 25:
                if ch == "a":
                    lexeme += self.advance()
                    state = 26
                else:
                    state = 256
            elif state == 26:
                if ch == "n":
                    lexeme += self.advance()
                    state = 27
                elif ch == "r":
                    lexeme += self.advance()
                    state = 30
                else:
                    state = 258
            elif state == 27:
                if ch == "t":
                    lexeme += self.advance()
                    state = 28
                else:
                    state = 260
            elif state == 28:
                if ch is None or ch in PAREN_DEL:
                    state = 29
                    return Token("chant", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 262
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # charge (30-32)
            elif state == 30:
                if ch == "g":
                    lexeme += self.advance()
                    state = 31
                else:
                    state = 260
            elif state == 31:
                if ch == "e":
                    lexeme += self.advance()
                    state = 32
                else:
                    state = 262
            elif state == 32:
                if ch is None or ch in PAREN_DEL:
                    state = 33
                    return Token("charge", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # circle (34-38)
            elif state == 34:
                if ch == "r":
                    lexeme += self.advance()
                    state = 35
                else:
                    state = 256
            elif state == 35:
                if ch == "c":
                    lexeme += self.advance()
                    state = 36
                else:
                    state = 258
            elif state == 36:
                if ch == "l":
                    lexeme += self.advance()
                    state = 37
                else:
                    state = 260
            elif state == 37:
                if ch == "e":
                    lexeme += self.advance()
                    state = 38
                else:
                    state = 262
            elif state == 38:
                if ch is None or ch in WHITESPACE:
                    state = 39
                    return Token("circle", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # counter (47-51)
            elif state == 40:
                if ch == "u":
                    lexeme += self.advance()
                    state = 41
                else:
                    state = 256
            elif state == 41:
                if ch == "n":
                    lexeme += self.advance()
                    state = 42
                else:
                    state = 258
            elif state == 42:
                if ch == "t":
                    lexeme += self.advance()
                    state = 43
                else:
                    state = 260
            elif state == 43:
                if ch == "e":
                    lexeme += self.advance()
                    state = 44
                else:
                    state = 262
            elif state == 44:
                if ch == "r":
                    lexeme += self.advance()
                    state = 45
                else:
                    state = 264
            elif state == 45:
                if ch is None or ch in CURLY_DEL:
                    state = 46
                    return Token("counter", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 266
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # crossroad (53-60)
            elif state == 47:
                if ch == "o":
                    lexeme += self.advance()
                    state = 48
                else:
                    state = 256
            elif state == 48:
                if ch == "s":
                    lexeme += self.advance()
                    state = 49
                else:
                    state = 258
            elif state == 49:
                if ch == "s":
                    lexeme += self.advance()
                    state = 50
                else:
                    state = 260
            elif state == 50:
                if ch == "r":
                    lexeme += self.advance()
                    state = 51
                else:
                    state = 262
            elif state == 51:
                if ch == "o":
                    lexeme += self.advance()
                    state = 52
                else:
                    state = 264
            elif state == 52:
                if ch == "a":
                    lexeme += self.advance()
                    state = 53
                else:
                    state = 266
            elif state == 53:
                if ch == "d":
                    lexeme += self.advance()
                    state = 54
                else:
                    state = 268
            elif state == 54:
                if ch is None or ch in PAREN_DEL:
                    state = 55
                    return Token("crossroad", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 270
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # cursed (62-66)
            elif state == 56:
                if ch == "r":
                    lexeme += self.advance()
                    state = 57
                else:
                    state = 256
            elif state == 57:
                if ch == "s":
                    lexeme += self.advance()
                    state = 58
                else:
                    state = 258
            elif state == 58:
                if ch == "e":
                    lexeme += self.advance()
                    state = 59
                else:
                    state = 260
            elif state == 59:
                if ch == "d":
                    lexeme += self.advance()
                    state = 60
                else:
                    state = 262
            elif state == 60:
                if ch is None or ch in AURA_LIT_DEL:
                    state = 61
                    return Token("cursed", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # darkness (68-76)
            elif state == 62:
                if ch == "a":
                    lexeme += self.advance()
                    state = 63
                else:
                    state = 254
            elif state == 63:
                if ch == "r":
                    lexeme += self.advance()
                    state = 64
                else:
                    state = 256
            elif state == 64:
                if ch == "k":
                    lexeme += self.advance()
                    state = 65
                else:
                    state = 258
            elif state == 65:
                if ch == "n":
                    lexeme += self.advance()
                    state = 66
                else:
                    state = 260
            elif state == 66:
                if ch == "e":
                    lexeme += self.advance()
                    state = 67
                else:
                    state = 262
            elif state == 67:
                if ch == "s":
                    lexeme += self.advance()
                    state = 68
                else:
                    state = 264
            elif state == 68:
                if ch == "s":
                    lexeme += self.advance()
                    state = 69
                else:
                    state = 266
            elif state == 69:
                if ch is None or ch in WHITESPACE:
                    state = 70
                    return Token("darkness", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 268
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # essence (77-76)
            elif state == 71:
                if ch == "s":
                    lexeme += self.advance()
                    state = 72
                else:
                    state = 254
            elif state == 72:
                if ch == "s":
                    lexeme += self.advance()
                    state = 73
                else:
                    state = 256
            elif state == 73:
                if ch == "e":
                    lexeme += self.advance()
                    state = 74
                else:
                    state = 258
            elif state == 74:
                if ch == "n":
                    lexeme += self.advance()
                    state = 75
                else:
                    state = 260
            elif state == 75:
                if ch == "c":
                    lexeme += self.advance()
                    state = 76
                else:
                    state = 262
            elif state == 76:
                if ch == "e":
                    lexeme += self.advance()
                    state = 77
                else:
                    state = 264
            elif state == 77:
                if ch is None or ch in WHITESPACE:
                    state = 78
                    return Token("essence", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 266
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # fallback (85-93)
            elif state == 79:
                if ch == "a":
                    lexeme += self.advance()
                    state = 80
                else:
                    state = 254
            elif state == 80:
                if ch == "l":
                    lexeme += self.advance()
                    state = 81
                else:
                    state = 256
            elif state == 81:
                if ch == "l":
                    lexeme += self.advance()
                    state = 82
                else:
                    state = 258
            elif state == 82:
                if ch == "b":
                    lexeme += self.advance()
                    state = 83
                else:
                    state = 260
            elif state == 83:
                if ch == "a":
                    lexeme += self.advance()
                    state = 84
                else:
                    state = 262
            elif state == 84:
                if ch == "c":
                    lexeme += self.advance()
                    state = 85
                else:
                    state = 264
            elif state == 85:
                if ch == "k":
                    lexeme += self.advance()
                    state = 86
                else:
                    state = 266
            elif state == 86:
                if ch is None or ch in CURLY_DEL:
                    state = 87
                    return Token("fallback", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 268
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # grimoire (94-102)
            elif state == 88:
                if ch == "r":
                    lexeme += self.advance()
                    state = 89
                else:
                    state = 254
            elif state == 89:
                if ch == "i":
                    lexeme += self.advance()
                    state = 90
                else:
                    state = 256
            elif state == 90:
                if ch == "m":
                    lexeme += self.advance()
                    state = 91
                else:
                    state = 258
            elif state == 91:
                if ch == "o":
                    lexeme += self.advance()
                    state = 92
                else:
                    state = 260
            elif state == 92:
                if ch == "i":
                    lexeme += self.advance()
                    state = 93
                else:
                    state = 262
            elif state == 93:
                if ch == "r":
                    lexeme += self.advance()
                    state = 94
                else:
                    state = 264
            elif state == 94:
                if ch == "e":
                    lexeme += self.advance()
                    state = 95
                else:
                    state = 266
            elif state == 95:
                if ch is None or ch in PAREN_DEL:
                    state = 96
                    return Token("grimoire", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 268
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # INSCRIPTION (103-114), INVOKE (115-119)
            # inscription (103 - 113)
            elif state == 97:
                if ch == "n":
                    lexeme += self.advance()
                    state = 98
                else:
                    state = 254
            elif state == 98:
                if ch == "s":
                    lexeme += self.advance()
                    state = 99
                elif ch == "v":
                    lexeme += self.advance()
                    state = 109
                else:
                    state = 256
            elif state == 99:
                if ch == "c":
                    lexeme += self.advance()
                    state = 100
                else:
                    state = 258
            elif state == 100:
                if ch == "r":
                    lexeme += self.advance()
                    state = 101
                else:
                    state = 260
            elif state == 101:
                if ch == "i":
                    lexeme += self.advance()
                    state = 102
                else:
                    state = 262
            elif state == 102:
                if ch == "p":
                    lexeme += self.advance()
                    state = 103
                else:
                    state = 264
            elif state == 103:
                if ch == "t":
                    lexeme += self.advance()
                    state = 104
                else:
                    state = 266
            elif state == 104:
                if ch == "i":
                    lexeme += self.advance()
                    state = 105
                else:
                    state = 268
            elif state == 105:
                if ch == "o":
                    lexeme += self.advance()
                    state = 106
                else:
                    state = 270
            elif state == 106:
                if ch == "n":
                    lexeme += self.advance()
                    state = 107
                else:
                    state = 272
            elif state == 107:
                if ch is None or ch in WHITESPACE:
                    state = 108
                    return Token("inscription", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 274
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # invoke (115-118)
            elif state == 109:
                if ch == "o":
                    lexeme += self.advance()
                    state = 110
                else:
                    state = 258
            elif state == 110:
                if ch == "k":
                    lexeme += self.advance()
                    state = 111
                else:
                    state = 260
            elif state == 111:
                if ch == "e":
                    lexeme += self.advance()
                    state = 112
                else:
                    state = 262
            elif state == 112:
                if ch is None or ch in CURLY_DEL:
                    state = 113
                    return Token("invoke", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # manifest (200-208)
            elif state == 114:
                if ch == "a":
                    lexeme += self.advance()
                    state = 115
                else:
                    state = 254
            elif state == 115:
                if ch == "n":
                    lexeme += self.advance()
                    state = 116
                else:
                    state = 256
            elif state == 116:
                if ch == "i":
                    lexeme += self.advance()
                    state = 117
                else:
                    state = 258
            elif state == 117:
                if ch == "f":
                    lexeme += self.advance()
                    state = 118
                else:
                    state = 260
            elif state == 118:
                if ch == "e":
                    lexeme += self.advance()
                    state = 119
                else:
                    state = 262
            elif state == 119:
                if ch == "s":
                    lexeme += self.advance()
                    state = 120
                else:
                    state = 264
            elif state == 120:
                if ch == "t":
                    lexeme += self.advance()
                    state = 121
                else:
                    state = 266
            elif state == 121:
                if ch is None or ch in PAREN_DEL:
                    state = 122
                    return Token("manifest", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 268
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # null (209-213)
            elif state == 123:
                if ch == "u":
                    lexeme += self.advance()
                    state = 124
                else:
                    state = 254
            elif state == 124:
                if ch == "l":
                    lexeme += self.advance()
                    state = 125
                else:
                    state = 256
            elif state == 125:
                if ch == "l":
                    lexeme += self.advance()
                    state = 126
                else:
                    state = 258
            elif state == 126:
                if ch is None or ch in TRANSFER_DEL:
                    state = 127
                    return Token("null", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 260
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # persist (214-221)
            elif state == 128:
                if ch == "e":
                    lexeme += self.advance()
                    state = 129
                else:
                    state = 254
            elif state == 129:
                if ch == "r":
                    lexeme += self.advance()
                    state = 130
                else:
                    state = 256
            elif state == 130:
                if ch == "s":
                    lexeme += self.advance()
                    state = 131
                else:
                    state = 258
            elif state == 131:
                if ch == "i":
                    lexeme += self.advance()
                    state = 132
                else:
                    state = 260
            elif state == 132:
                if ch == "s":
                    lexeme += self.advance()
                    state = 133
                else:
                    state = 262
            elif state == 133:
                if ch == "t":
                    lexeme += self.advance()
                    state = 134
                else:
                    state = 264
            elif state == 134:
                if ch is None or ch in TRANSFER_DEL:
                    state = 135
                    return Token("persist", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 266
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # RUNE (142-146), REMANIFEST (147-156)
            elif state == 136:
                if ch == "u":
                    lexeme += self.advance()
                    state = 137
                elif ch == "e":
                    lexeme += self.advance()
                    state = 141
                else:
                    state = 254

            # rune (142-145)
            elif state == 137:
                if ch == "n":
                    lexeme += self.advance()
                    state = 138
                else:
                    state = 256
            elif state == 138:
                if ch == "e":
                    lexeme += self.advance()
                    state = 139
                else:
                    state = 258
            elif state == 139:
                if ch is None or ch in WHITESPACE:
                    state = 140
                    return Token("rune", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 260
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # remanifest (147-155)
            elif state == 141:
                if ch == "m":
                    lexeme += self.advance()
                    state = 142
                else:
                    state = 256
            elif state == 142:
                if ch == "a":
                    lexeme += self.advance()
                    state = 143
                else:
                    state = 258
            elif state == 143:
                if ch == "n":
                    lexeme += self.advance()
                    state = 144
                else:
                    state = 260
            elif state == 144:
                if ch == "i":
                    lexeme += self.advance()
                    state = 145
                else:
                    state = 262
            elif state == 145:
                if ch == "f":
                    lexeme += self.advance()
                    state = 146
                else:
                    state = 264
            elif state == 146:
                if ch == "e":
                    lexeme += self.advance()
                    state = 147
                else:
                    state = 266
            elif state == 147:
                if ch == "s":
                    lexeme += self.advance()
                    state = 148
                else:
                    state = 268
            elif state == 148:
                if ch == "t":
                    lexeme += self.advance()
                    state = 149
                else:
                    state = 270
            elif state == 149:
                if ch is None or ch in PAREN_DEL:
                    state = 150
                    return Token("remanifest", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 272
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # SCROLL (157-163), SEALED (164-169), SHATTER (170-176), SPELL (177-181), SUMMON (182-187)
            elif state == 151:
                if ch == "c":
                    lexeme += self.advance()
                    state = 152
                elif ch == "e":
                    lexeme += self.advance()
                    state = 158
                elif ch == "h":
                    lexeme += self.advance()
                    state = 164
                elif ch == "p":
                    lexeme += self.advance()
                    state = 171
                elif ch == "u":
                    lexeme += self.advance()
                    state = 176
                else:
                    state = 254

            # scroll (158-162)
            elif state == 152:
                if ch == "r":
                    lexeme += self.advance()
                    state = 153
                else:
                    state = 256
            elif state == 153:
                if ch == "o":
                    lexeme += self.advance()
                    state = 154
                else:
                    state = 258
            elif state == 154:
                if ch == "l":
                    lexeme += self.advance()
                    state = 155
                else:
                    state = 260
            elif state == 155:
                if ch == "l":
                    lexeme += self.advance()
                    state = 156
                else:
                    state = 262
            elif state == 156:
                if ch is None or ch in PAREN_DEL:
                    state = 157
                    return Token("scroll", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # sealed (164-168)
            elif state == 158:
                if ch == "a":
                    lexeme += self.advance()
                    state = 159
                else:
                    state = 256
            elif state == 159:
                if ch == "l":
                    lexeme += self.advance()
                    state = 160
                else:
                    state = 258
            elif state == 160:
                if ch == "e":
                    lexeme += self.advance()
                    state = 161
                else:
                    state = 260
            elif state == 161:
                if ch == "d":
                    lexeme += self.advance()
                    state = 162
                else:
                    state = 262
            elif state == 162:
                if ch is None or ch in WHITESPACE:
                    state = 163
                    return Token("sealed", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # shatter (170-175)
            elif state == 164:
                if ch == "a":
                    lexeme += self.advance()
                    state = 165
                else:
                    state = 256
            elif state == 165:
                if ch == "t":
                    lexeme += self.advance()
                    state = 166
                else:
                    state = 258
            elif state == 166:
                if ch == "t":
                    lexeme += self.advance()
                    state = 167
                else:
                    state = 260
            elif state == 167:
                if ch == "e":
                    lexeme += self.advance()
                    state = 168
                else:
                    state = 262
            elif state == 168:
                if ch == "r":
                    lexeme += self.advance()
                    state = 169
                else:
                    state = 264
            elif state == 169:
                if ch is None or ch in TRANSFER_DEL:
                    state = 170
                    return Token("shatter", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 266
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # spell (177-180)
            elif state == 171:
                if ch == "e":
                    lexeme += self.advance()
                    state = 172
                else:
                    state = 256
            elif state == 172:
                if ch == "l":
                    lexeme += self.advance()
                    state = 173
                else:
                    state = 258
            elif state == 173:
                if ch == "l":
                    lexeme += self.advance()
                    state = 174
                else:
                    state = 260
            elif state == 174:
                if ch is None or ch in WHITESPACE:
                    state = 175
                    return Token("spell", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 262
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # summon (182-186)
            elif state == 176:
                if ch == "m":
                    lexeme += self.advance()
                    state = 177
                else:
                    state = 256
            elif state == 177:
                if ch == "m":
                    lexeme += self.advance()
                    state = 178
                else:
                    state = 258
            elif state == 178:
                if ch == "o":
                    lexeme += self.advance()
                    state = 179
                else:
                    state = 260
            elif state == 179:
                if ch == "n":
                    lexeme += self.advance()
                    state = 180
                else:
                    state = 262
            elif state == 180:
                if ch is None or ch in WHITESPACE:
                    state = 181
                    return Token("summon", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 264
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # yield (188-193)
            elif state == 182:
                if ch == "i":
                    lexeme += self.advance()
                    state = 183
                else:
                    state = 254
            elif state == 183:
                if ch == "e":
                    lexeme += self.advance()
                    state = 184
                else:
                    state = 256
            elif state == 184:
                if ch == "l":
                    lexeme += self.advance()
                    state = 185
                else:
                    state = 258
            elif state == 185:
                if ch == "d":
                    lexeme += self.advance()
                    state = 186
                else:
                    state = 260
            elif state == 186:
                if ch is None or ch in TRANSFER_DEL:
                    state = 187
                    return Token("yield", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    state = 262
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after keyword '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # IDENTIFIER STATES: 254-284
            elif 254 <= state <= 284 and state % 2 == 0:
                if ch in ID_DEL or ch is None:
                    state = state + 1
                    return Token("id", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    if state == 284:
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
                if ch == ")":
                    lexeme += self.advance()
                    state = 188
                elif ch == "(":
                    lexeme += self.advance()
                    state = 190
                elif ch == "}":
                    lexeme += self.advance()
                    state = 192
                elif ch == "{":
                    lexeme += self.advance()
                    state = 194
                elif ch == "[":
                    lexeme += self.advance()
                    state = 196
                elif ch == "]":
                    lexeme += self.advance()
                    state = 198
                elif ch == "~":
                    lexeme += self.advance()
                    state = 200
                elif ch == "+":
                    lexeme += self.advance()
                    state = 202
                elif ch == "-":
                    lexeme += self.advance()
                    state = 208
                elif ch == "*":
                    lexeme += self.advance()
                    state = 214
                elif ch == "/":
                    lexeme += self.advance()
                    state = 218
                elif ch == "%":
                    lexeme += self.advance()
                    state = 222
                elif ch == ">":
                    lexeme += self.advance()
                    state = 226
                elif ch == "<":
                    lexeme += self.advance()
                    state = 230
                elif ch == "=":
                    lexeme += self.advance()
                    state = 234
                elif ch == "!":
                    lexeme += self.advance()
                    state = 238
                elif ch == "&":
                    lexeme += self.advance()
                    state = 242
                elif ch == "|":
                    lexeme += self.advance()
                    state = 245
                elif ch == ".":
                    lexeme += self.advance()
                    state = 248
                elif ch == ";":
                    lexeme += self.advance()
                    state = 250
                elif ch == ",":
                    lexeme += self.advance()
                    state = 252
                else:
                    raise LexerError(
                        f"Unexpected symbol character {repr(ch)}", self.line, start_col
                    )

            

            # ')' (196 -> 197*)
            elif state == 188:
                if ch is None or ch in CLOSE_PAREN_DEL:
                    state = 189
                    return Token(")", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ')'", self.line, self.col
                )

            # '(' (194 -> 195*)
            elif state == 190:
                if ch in OPEN_PAREN_DEL:
                    state = 191
                    return Token("(", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '('", self.line, self.col
                )

            # '}' (200 -> 201*)
            elif state == 192:
                if ch is None or ch in CLOSE_CURLY_DEL:
                    state = 193
                    return Token("}", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '}}'", self.line, self.col
                )

            # '{' (198 -> 199*)
            elif state == 194:
                if ch in OPEN_CURLY_DEL:
                    state = 195
                    return Token("{", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '{{'", self.line, self.col
                )
            
            # '[' (202 -> 203*)
            elif state == 196:
                if ch in OPEN_BRACKET_DEL:
                    state = 197
                    return Token("[", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '['", self.line, self.col
                )

            # ']' (204 -> 205*)
            elif state == 198:
                if ch is None or ch in CLOSE_BRACKET_DEL:
                    state = 199
                    return Token("]", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ']'", self.line, self.col
                )

            # '~' (206 -> 207*)
            elif state == 200:
                if ch in NEG_DEL:
                    state = 201
                    return Token("~", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '~'", self.line, self.col
                )

            # '+' branch (208 -> 213*)
            elif state == 202:
                if ch == "+":
                    lexeme += self.advance()
                    state = 204
                elif ch == "=":
                    lexeme += self.advance()
                    state = 206
                elif ch in MATH_DEL:
                    state = 203
                    return Token("+", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '+'", self.line, self.col
                    )

            # '++' (210 -> 211*)
            elif state == 204:
                if ch is None or ch in CREMENT_DEL:
                    state = 205
                    return Token("++", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '++'", self.line, self.col
                )

            # '+=' (212 -> 213*)
            elif state == 206:
                if ch in ASSIGN_DEL:
                    state = 207
                    return Token("+=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '+='", self.line, self.col
                )

            # '-' branch (214 -> 219*)
            elif state == 208:
                if ch == "-":
                    lexeme += self.advance()
                    state = 210
                elif ch == "=":
                    lexeme += self.advance()
                    state = 212
                elif ch in MATH_DEL:
                    state = 209
                    return Token("-", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '-'", self.line, self.col
                    )

            # '--' (216 -> 217*)
            elif state == 210:
                if ch is None or ch in CREMENT_DEL:
                    state = 211
                    return Token("--", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '--'", self.line, self.col
                )

            # '-=' (218 -> 219*)
            elif state == 212:
                if ch in ASSIGN_DEL:
                    state = 213
                    return Token("-=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '-='", self.line, self.col
                )

            # '*' branch (220 -> 223*)
            elif state == 214:
                if ch == "=":
                    lexeme += self.advance()
                    state = 216
                elif ch in MATH_DEL:
                    state = 215
                    return Token("*", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '*'", self.line, self.col
                    )

            # '*=' (222 -> 223*)
            elif state == 216:
                if ch in ASSIGN_DEL:
                    state = 217
                    return Token("*=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '*='", self.line, self.col
                )

            # '/' branch (224 -> 227*)
            elif state == 218:
                if ch == "=":
                    lexeme += self.advance()
                    state = 220
                elif ch in MATH_DEL:
                    state = 223
                    return Token("/", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '/'", self.line, self.col
                    )

            # '/=' (226 -> 227*)
            elif state == 220:
                if ch in ASSIGN_DEL:
                    state = 221
                    return Token("/=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '/='", self.line, self.col
                )

            # '%' branch (228 -> 231*)
            elif state == 222:
                if ch == "=":
                    lexeme += self.advance()
                    state = 224
                elif ch in MATH_DEL:
                    state = 223
                    return Token("%", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '%'", self.line, self.col
                    )

            # '%=' (230 -> 231*)
            elif state == 224:
                if ch in ASSIGN_DEL:
                    state = 225
                    return Token("%=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '%='", self.line, self.col
                )

            # '>' branch (232 -> 235*)
            elif state == 226:
                if ch == "=":
                    lexeme += self.advance()
                    state = 228
                elif ch in REL_DEL:
                    state = 227
                    return Token(">", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '>'", self.line, self.col
                    )

            # '>=' (234 -> 235*)
            elif state == 228:
                if ch in REL_DEL:
                    state = 229
                    return Token(">=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '>='", self.line, self.col
                )

            # '<' branch (236 -> 239*)
            elif state == 230:
                if ch == "=":
                    lexeme += self.advance()
                    state = 232
                elif ch in REL_DEL:
                    state = 231
                    return Token("<", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '<'", self.line, self.col
                    )

            # '<=' (238 -> 239*)
            elif state == 232:
                if ch in REL_DEL:
                    state = 233
                    return Token("<=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '<='", self.line, self.col
                )

            # '=' branch (240 -> 243*)
            elif state == 234:
                if ch == "=":
                    lexeme += self.advance()
                    state = 236
                elif ch in BASE_ASSIGN_DEL:
                    state = 235
                    return Token("=", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '='", self.line, self.col
                    )

            # '==' (242 -> 243*)
            elif state == 236:
                if ch in EQUALITY_DEL:
                    state = 237
                    return Token("==", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '=='", self.line, self.col
                )

            # '!' branch (244 -> 247*)
            elif state == 238:
                if ch == "=":
                    lexeme += self.advance()
                    state = 240
                elif ch in NOT_DEL:
                    state = 239
                    return Token("!", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '!'", self.line, self.col
                    )

            # '!=' (246 -> 247*)
            elif state == 240:
                if ch in EQUALITY_DEL:
                    state = 241
                    return Token("!=", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '!='", self.line, self.col
                )

            # '&&' (248 -> 250*)
            elif state == 242:
                if ch == "&":
                    lexeme += self.advance()
                    state = 243
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' after '&'. Expected '&&'",
                        self.line,
                        self.col,
                    )

            elif state == 243:
                if ch in LOG_DEL:
                    state = 244
                    return Token("&&", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '&&'", self.line, self.col
                )

            # '||' (251 -> 253*)
            elif state == 245:
                if ch == "|":
                    lexeme += self.advance()
                    state = 246
                else:
                    raise LexerError(
                        f"Unexpected character '{ch}' after '|'. Expected '||'",
                        self.line,
                        self.col,
                    )

            elif state == 246:
                if ch in LOG_DEL:
                    state = 247
                    return Token("||", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '||'", self.line, self.col
                )

            # '.' (254 -> 255*)
            elif state == 248:
                if ch in LETTERS:
                    state = 249
                    return Token(".", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after '.'", self.line, self.col
                )

            # ';' (256 -> 257*)
            elif state == 250:
                if ch is None or ch in SPACE_DEL:
                    state = 251
                    return Token(";", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ';'", self.line, self.col
                )

            # ',' (258 -> 259*)
            elif state == 252:
                if ch in COMMA_DEL:
                    state = 253
                    return Token(",", lexeme, self.line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after ','", self.line, self.col
                )

# ========== LITERALS SCANNER ==========
    def scan_number(self) -> Token:
        state = 0
        start_col = self.col
        lexeme = ""

        while True:
            ch = self.current()

            # ROOT STATE 0: '0' -> 286, or optional '~' (or nothing) -> 288
            if state == 0:
                if ch == "0":
                    lexeme += self.advance()
                    state = 286
                elif ch == "~":
                    lexeme += self.advance()
                    state = 288
                elif ch is not None and ch in NONZERO:
                    lexeme += self.advance()
                    state = 290
                else:
                    raise LexerError(
                        f"Unexpected character {repr(ch)} in number",
                        self.line,
                        start_col,
                    )

            # after '~' (288): '0' -> 289, nonzero -> 290
            elif state == 288:
                if ch == "0":
                    lexeme += self.advance()
                    state = 289
                elif ch is not None and ch in NONZERO:
                    lexeme += self.advance()
                    state = 290
                else:
                    raise LexerError(
                        f"Expected a digit after '~' in '{lexeme}'", self.line, self.col
                    )

            # '~0' (289): only valid as the start of a float ('~0.'), never as an aether literal
            elif state == 289:
                if ch == ".":
                    lexeme += self.advance()
                    state = 321
                elif ch is not None and ch in NUMBERS:
                    raise LexerError(
                        f"Leading zeros are not allowed ('{lexeme}{ch}')",
                        self.line,
                        start_col,
                        skip_number=True,
                    )
                else:
                    raise LexerError(
                        f"'{lexeme}' must be followed by '.' (negative zero is not a valid aether literal)",
                        self.line,
                        self.col,
                    )

            # '0' (286 -> 287*) or '0.' (-> 321)
            elif state == 286:
                if ch == ".":
                    lexeme += self.advance()
                    state = 321
                elif ch is None or ch in AETHER_LIT_DEL:
                    state = 287
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

            elif state == 290 or (291 <= state <= 319 and state % 2 == 1):
                if ch is not None and ch in NUMBERS:
                    if state == 319:
                        raise LexerError(
                            f"'{lexeme}' has invalid delimiter '{ch}'",
                            self.line,
                            self.col,
                        )
                    lexeme += self.advance()
                    state = 291 if state == 290 else state + 2
                elif ch == ".":
                    lexeme += self.advance()
                    state = 321
                elif ch is None or ch in AETHER_LIT_DEL:
                    state = state + 1
                    return Token("aeth_lit", lexeme, self.line, start_col)
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after aether literal '{lexeme}'",
                        self.line,
                        self.col,
                    )

            # after '.' (321): need at least one fractional digit.
            elif state == 321:
                if ch is not None and ch in NUMBERS:
                    lexeme += self.advance()
                    frac_len = 1
                    state = 323
                else:
                    raise LexerError(
                        f"Expected a digit after '.' in '{lexeme}'", self.line, self.col
                    )

            # fractional digits (323): consumed with the frac_len counter
            # any digit may be consumed (the 'numbers' edge), the literal may only END on a
            # nonzero digit (the 'nonzero' edge), except the lone ".0".
            elif state == 323:
                if ch is not None and ch in NUMBERS:
                    if frac_len == 8:
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
        state = 0
        start_line = self.line
        start_col = self.col
        lexeme = ""
        bad = False  # an invalid escape/character was found; the string is still read to its end

        while True:
            ch = self.current()

            if state == 0:
                if ch == '"':
                    lexeme += self.advance()
                    state = 347
                else:
                    raise LexerError(
                        f"Unexpected character {repr(ch)} (expected '\"')",
                        self.line,
                        start_col,
                    )

            elif state == 347:
                if ch is None or ch in NEWLINE:
                    raise LexerError(
                        f"Unterminated inscription literal: {lexeme!r}",
                        start_line,
                        start_col,
                    )
                elif ch == '"':
                    lexeme += self.advance()
                    state = 348
                elif ch == "\\":
                    lexeme += self.advance()
                    esc = self.current()
                    if esc is None or esc in NEWLINE:
                        raise LexerError(
                            f"Unterminated inscription literal: {lexeme!r}",
                            start_line,
                            start_col,
                        )
                    if esc not in ESCAPE_CHARS:
                        self.errors.append(
                            LexerError(
                                f"Invalid escape sequence '\\{esc}'",
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
                            f"Invalid character {repr(ch)} in inscription literal",
                            self.line,
                            self.col,
                        )
                    )
                    bad = True
                    lexeme += self.advance()

            elif state == 348:
                if ch is None or ch in INSCRIPTION_LIT_DEL:
                    state = 349
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
        state = 0
        start_line = self.line
        start_col = self.col
        lexeme = ""

        while True:
            ch = self.current()

            if state == 0:
                if ch == "#":
                    lexeme += self.advance()
                    state = 350
                else:
                    raise LexerError(
                        f"Unexpected character {repr(ch)} (expected '#/')",
                        self.line,
                        start_col,
                    )

            elif state == 350:
                if ch == "/":
                    lexeme += self.advance()
                    state = 351
                else:
                    raise LexerError(
                        f"Invalid delimiter '{ch}' after '#'", self.line, self.col
                    )

            elif state == 351:
                if ch is None:
                    raise LexerError(
                        f"Unterminated comment: {lexeme!r}", start_line, start_col
                    )
                elif ch == "/":
                    lexeme += self.advance()
                    state = 352
                elif ch in ASCII:
                    lexeme += self.advance()
                else:
                    # report it, but stay inside the comment so the rest isn't tokenized as code
                    self.errors.append(
                        LexerError(
                            f"Invalid character {repr(ch)} in comment",
                            self.line,
                            self.col,
                        )
                    )
                    lexeme += self.advance()

            elif state == 352:
                if ch == "#":
                    lexeme += self.advance()
                    state = 353
                else:
                    state = 351

            elif state == 353:
                if ch is None or ch in SPACE_DEL:
                    state = 354
                    return Token("COMMENT", lexeme, start_line, start_col)
                raise LexerError(
                    f"Invalid delimiter '{ch}' after comment", self.line, self.col
                )

    # ========== TOKENIZER ==========
    def tokenize(self) -> List[Token]:
        """Scans the whole source. Lexical errors are collected in self.errors instead of stopping the scan."""
        while True:
            ch = self.current()
            if ch is None:
                break
            if ch in WHITESPACE or ch in NEWLINE:
                self.advance()
                continue

            start_pos = self.pos
            try:
                if ch in LETTERS:
                    token = self.scan_word()
                elif ch in NUMBERS or (ch == "~" and self.peek() in NUMBERS):
                    token = self.scan_number()
                elif ch in OPEN_QUOTE:
                    token = self.scan_string()
                elif ch == "#" and self.peek() == "/":
                    token = self.scan_comment()
                else:
                    token = self.scan_symbol()
            except LexerError as err:
                self.errors.append(err)
                self.recover(err, start_pos)
                continue

            if token is not None and token.type != "COMMENT":
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
