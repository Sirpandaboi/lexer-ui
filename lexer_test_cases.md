# Lexer limit test cases

Paste each code block into the UI and compare with **Expected**.

- ✅ = lexes cleanly (the token list is what you should see)
- ❌ = must produce the error shown (line/col are for the block exactly as written)
- 🕳️ = **known hole**: the lexer currently does NOT do the desired thing (section 11)
- ⚠ *Exact input* = the block contains invisible characters (tab, CR, form feed, non-breaking space, trailing newline); paste the escaped Python string instead

## 1. Identifier limits

### 1.1 1 char

```
a
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.2 16 chars (max)

```
abcdefghabcdefgh
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.3 17 chars (one over)

```
abcdefghabcdefghi
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 17: 'abcdefghabcdefgh' has invalid delimiter 'i']`
- tokens still produced: IDENTIFIER

### 1.4 40 chars

```
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 17: 'aaaaaaaaaaaaaaaa' has invalid delimiter 'a']`
- `Lexical Error [Line 1, Col 33: 'aaaaaaaaaaaaaaaa' has invalid delimiter 'a']`
- tokens still produced: IDENTIFIER

### 1.5 underscore + digits inside

```
a_1_b_2
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.6 ends in underscore

```
abc_
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.7 starts with underscore

```
_abc
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '_']`
- tokens still produced: IDENTIFIER

### 1.8 starts with digit

```
1abc
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter 'a' after aether literal '1']`
- tokens still produced: IDENTIFIER

### 1.9 uppercase is not a keyword

```
Aether
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.10 keyword prefix is identifier

```
aeth
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.11 keyword + suffix is identifier

```
aethers
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.12 keyword + underscore is identifier

```
cast_
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.13 16-char keyword-prefixed identifier

```
inscriptionzzzzz
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

### 1.14 17-char keyword-prefixed identifier

```
inscriptionzzzzzz
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 17: 'inscriptionzzzzz' has invalid delimiter 'z']`
- tokens still produced: IDENTIFIER

### 1.15 identifier then bad char

```
abc@
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '@' after identifier 'abc']`

### 1.16 identifier + non-ASCII

```
abcé
```

⚠ Exact input: `'abcé'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter 'é' after identifier 'abc']`

## 2. Keywords & delimiters

### 2.1 aether + space

```
aether x;
```

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_TERMINATOR

### 2.2 aether + tab

```
aether	x;
```

⚠ Exact input: `'aether\tx;'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_TERMINATOR

### 2.3 aether at EOF

```
aether
```

**Expected:** ✅ no errors — tokens: RW_AETHER

### 2.4 aether + ';' (not allowed)

```
aether;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 7: Invalid delimiter ';' after keyword 'aether']`
- tokens still produced: RS_TERMINATOR

### 2.5 essence + space

```
essence e;
```

**Expected:** ✅ no errors — tokens: RW_ESSENCE IDENTIFIER RS_TERMINATOR

### 2.6 inscription + space

```
inscription s;
```

**Expected:** ✅ no errors — tokens: RW_INSCRIPTION IDENTIFIER RS_TERMINATOR

### 2.7 aura + space

```
aura a;
```

**Expected:** ✅ no errors — tokens: RW_AURA IDENTIFIER RS_TERMINATOR

### 2.8 rune + space

```
rune r;
```

**Expected:** ✅ no errors — tokens: RW_RUNE IDENTIFIER RS_TERMINATOR

### 2.9 darkness + space

```
darkness d;
```

**Expected:** ✅ no errors — tokens: RW_DARKNESS IDENTIFIER RS_TERMINATOR

### 2.10 sealed + space

```
sealed x;
```

**Expected:** ✅ no errors — tokens: RW_SEALED IDENTIFIER RS_TERMINATOR

### 2.11 blessed;

```
blessed;
```

**Expected:** ✅ no errors — tokens: RW_BLESSED RS_TERMINATOR

### 2.12 cursed)

```
cursed)
```

**Expected:** ✅ no errors — tokens: RW_CURSED RS_CLOSE_PARENTHESIS

### 2.13 null,

```
null,
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 6: Invalid delimiter 'None' after ',']`
- tokens still produced: RW_NULL

### 2.14 cast(

```
cast(x)
```

**Expected:** ✅ no errors — tokens: RW_CAST RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.15 chant (space before paren)

```
chant (x)
```

**Expected:** ✅ no errors — tokens: RW_CHANT RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.16 charge(

```
charge(x)
```

**Expected:** ✅ no errors — tokens: RW_CHARGE RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.17 crossroad(

```
crossroad(x)
```

**Expected:** ✅ no errors — tokens: RW_CROSSROAD RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.18 scroll(

```
scroll(x)
```

**Expected:** ✅ no errors — tokens: RW_SCROLL RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.19 grimoire(

```
grimoire(x)
```

**Expected:** ✅ no errors — tokens: RW_GRIMOIRE RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.20 manifest(

```
manifest(x)
```

**Expected:** ✅ no errors — tokens: RW_MANIFEST RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.21 remanifest(

```
remanifest(x)
```

**Expected:** ✅ no errors — tokens: RW_REMANIFEST RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 2.22 counter{

```
counter{}
```

**Expected:** ✅ no errors — tokens: RW_COUNTER RS_OPEN_CURLY_BRACE RS_CLOSE_CURLY_BRACE

### 2.23 fallback{

```
fallback{}
```

**Expected:** ✅ no errors — tokens: RW_FALLBACK RS_OPEN_CURLY_BRACE RS_CLOSE_CURLY_BRACE

### 2.24 invoke{

```
invoke{}
```

**Expected:** ✅ no errors — tokens: RW_INVOKE RS_OPEN_CURLY_BRACE RS_CLOSE_CURLY_BRACE

### 2.25 persist;

```
persist;
```

**Expected:** ✅ no errors — tokens: RW_PERSIST RS_TERMINATOR

### 2.26 shatter;

```
shatter;
```

**Expected:** ✅ no errors — tokens: RW_SHATTER RS_TERMINATOR

### 2.27 yield;

```
yield;
```

**Expected:** ✅ no errors — tokens: RW_YIELD RS_TERMINATOR

### 2.28 yield x;

```
yield x;
```

**Expected:** ✅ no errors — tokens: RW_YIELD IDENTIFIER RS_TERMINATOR

### 2.29 spell + space

```
spell f
```

**Expected:** ✅ no errors — tokens: RW_SPELL IDENTIFIER

### 2.30 summon + space

```
summon f
```

**Expected:** ✅ no errors — tokens: RW_SUMMON IDENTIFIER

### 2.31 circle + space

```
circle x
```

**Expected:** ✅ no errors — tokens: RW_CIRCLE IDENTIFIER

### 2.32 cursed (the keyword, not 'curse')

```
curse
```

**Expected:** ✅ no errors — tokens: IDENTIFIER

## 3. Aether literals

### 3.1 0

```
0;
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_TERMINATOR

### 3.2 1 digit

```
7;
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_TERMINATOR

### 3.3 16 digits (max)

```
1234567890123456;
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_TERMINATOR

### 3.4 17 digits (one over)

```
12345678901234567;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 17: '1234567890123456' has invalid delimiter '7']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 3.5 30 digits

```
111111111111111111111111111111;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 17: '1111111111111111' has invalid delimiter '1']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 3.6 negative

```
~5;
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_TERMINATOR

### 3.7 negative 16 digits

```
~1234567890123456;
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_TERMINATOR

### 3.8 negative 17 digits

```
~12345678901234567;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 18: '~1234567890123456' has invalid delimiter '7']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 3.9 negative zero

```
~0;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: '~0' must be followed by '.' (negative zero is not a valid aether literal)]`
- tokens still produced: RS_TERMINATOR

### 3.10 leading zero 01

```
01;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Leading zeros are not allowed ('01')]`
- tokens still produced: RS_TERMINATOR

### 3.11 leading zero 007

```
007;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Leading zeros are not allowed ('00')]`
- tokens still produced: RS_TERMINATOR

### 3.12 leading zero ~01

```
~01;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Leading zeros are not allowed ('~01')]`
- tokens still produced: RS_TERMINATOR

### 3.13 double negative

```
~~5;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter '~' after '~']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 3.14 lone tilde

```
~;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter ';' after '~']`
- tokens still produced: RS_TERMINATOR

### 3.15 digit then letter

```
5a;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter 'a' after aether literal '5']`
- tokens still produced: IDENTIFIER RS_TERMINATOR

### 3.16 digit then underscore

```
5_;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter '_' after aether literal '5']`
- tokens still produced: RS_TERMINATOR

### 3.17 followed by ')'

```
5)
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_CLOSE_PARENTHESIS

### 3.18 followed by ']'

```
5]
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_CLOSE_BRACKET

### 3.19 followed by '}'

```
5}
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_CLOSE_CURLY_BRACE

### 3.20 followed by ','

```
5,6
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_COMMA AETHER_LITERAL

### 3.21 followed by newline

```
5
;
```

**Expected:** ✅ no errors — tokens: AETHER_LITERAL RS_TERMINATOR

### 3.22 followed by '('

```
5(
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter '(' after aether literal '5']`
- `Lexical Error [Line 1, Col 3: Invalid delimiter 'None' after '(']`

### 3.23 followed by '"'

```
5"a"
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter '"' after aether literal '5']`
- tokens still produced: LIT_INSCRIPTION

## 4. Essence literals

### 4.1 0.0 (lone zero allowed)

```
0.0;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.2 1.0

```
1.0;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.3 0.5

```
0.5;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.4 ~0.5

```
~0.5;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.5 ~0.0

```
~0.0;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.6 8 fractional digits (max)

```
1.12345678;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.7 9 fractional digits (one over)

```
1.123456789;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 11: '1.12345678' has invalid delimiter '9']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 4.8 16 int digits + 8 frac digits (max)

```
1234567890123456.12345678;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.9 17 int digits + frac

```
12345678901234567.5;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 17: '1234567890123456' has invalid delimiter '7']`
- tokens still produced: ESSENCE_LITERAL RS_TERMINATOR

### 4.10 ends in 0: 1.10

```
1.10;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Essence literal '1.10' cannot end in 0]`
- tokens still produced: RS_TERMINATOR

### 4.11 ends in 0: 1.00

```
1.00;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Essence literal '1.00' cannot end in 0]`
- tokens still produced: RS_TERMINATOR

### 4.12 ends in 0: 1.500

```
1.500;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Essence literal '1.500' cannot end in 0]`
- tokens still produced: RS_TERMINATOR

### 4.13 zeros inside ok: 1.00001

```
1.00001;
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_TERMINATOR

### 4.14 8 digits ending in 0

```
1.12345670;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Essence literal '1.12345670' cannot end in 0]`
- tokens still produced: RS_TERMINATOR

### 4.15 trailing dot: 5.

```
5.;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Expected a digit after '.' in '5.']`
- tokens still produced: RS_TERMINATOR

### 4.16 leading dot: .5

```
.5;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter '5' after '.']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 4.17 two dots: 5.5.5

```
5.5.5;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '.' after essence literal '5.5']`
- `Lexical Error [Line 1, Col 5: Invalid delimiter '5' after '.']`
- tokens still produced: AETHER_LITERAL RS_TERMINATOR

### 4.18 5.a

```
5.a;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Expected a digit after '.' in '5.']`
- tokens still produced: IDENTIFIER RS_TERMINATOR

### 4.19 ~0.

```
~0.;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Expected a digit after '.' in '~0.']`
- tokens still produced: RS_TERMINATOR

### 4.20 00.5

```
00.5;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Leading zeros are not allowed ('00')]`
- tokens still produced: RS_TERMINATOR

### 4.21 essence then ')'

```
1.5)
```

**Expected:** ✅ no errors — tokens: ESSENCE_LITERAL RS_CLOSE_PARENTHESIS

### 4.22 essence then ','

```
1.5,
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 5: Invalid delimiter 'None' after ',']`
- tokens still produced: ESSENCE_LITERAL

### 4.23 essence then letter

```
1.5a;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter 'a' after essence literal '1.5']`
- tokens still produced: IDENTIFIER RS_TERMINATOR

### 4.24 essence then ']' (inconsistent w/ aether)

```
x[1.5]
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 6: Invalid delimiter ']' after essence literal '1.5']`
- tokens still produced: IDENTIFIER RS_OPEN_BRACKET RS_CLOSE_BRACKET

### 4.25 no exponent support: 1.5e3

```
1.5e3;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter 'e' after essence literal '1.5']`
- tokens still produced: IDENTIFIER RS_TERMINATOR

## 5. Inscription literals

### 5.1 empty string

```
"";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.2 simple

```
"hello";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.3 spaces inside

```
"a b  c";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.4 all valid escapes

```
"\n\t\r\\\"";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.5 escaped quote inside

```
"say \"hi\"";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.6 invalid escape \q

```
"a\qb";
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid escape sequence '\q']`
- tokens still produced: RS_TERMINATOR

### 5.7 invalid escape \0

```
"a\0";
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid escape sequence '\0']`
- tokens still produced: RS_TERMINATOR

### 5.8 backslash at end then EOF

```
"abc\
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated inscription literal: '"abc\\']`

### 5.9 unterminated at EOF

```
"abc
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated inscription literal: '"abc']`

### 5.10 unterminated at newline

```
"abc
def";
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated inscription literal: '"abc']`
- `Lexical Error [Line 2, Col 4: Invalid delimiter '"' after identifier 'def']`
- `Lexical Error [Line 2, Col 4: Unterminated inscription literal: '";']`

### 5.11 tab inside string

```
"a	b";
```

⚠ Exact input: `'"a\tb";'`

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.12 non-ASCII inside

```
"café";
```

⚠ Exact input: `'"café";'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 5: Invalid character 'é' in inscription literal]`
- tokens still produced: RS_TERMINATOR

### 5.13 emoji inside

```
"hi 😀";
```

⚠ Exact input: `'"hi 😀";'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 5: Invalid character '😀' in inscription literal]`
- tokens still produced: RS_TERMINATOR

### 5.14 symbols inside

```
"!@#$%^&*()_+-=[]{}|;:,.<>?/";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

### 5.16 string then ')'

```
"a")
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_CLOSE_PARENTHESIS

### 5.17 string then ','

```
"a",
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 5: Invalid delimiter 'None' after ',']`
- tokens still produced: LIT_INSCRIPTION

### 5.18 string then '}'

```
"a"}
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_CLOSE_CURLY_BRACE

### 5.19 string then letter

```
"a"b
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter 'b' after inscription literal]`
- tokens still produced: IDENTIFIER

### 5.20 string then '+' no space

```
"a"+"b"
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '+' after inscription literal]`
- `Lexical Error [Line 1, Col 5: Invalid delimiter '"' after '+']`
- tokens still produced: LIT_INSCRIPTION

### 5.21 string + string with spaces

```
"a" + "b"
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_ADD LIT_INSCRIPTION

### 5.22 two strings no space

```
"a""b"
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '"' after inscription literal]`
- tokens still produced: LIT_INSCRIPTION

### 5.23 single-quote string

```
'a'
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character "'"]`
- `Lexical Error [Line 1, Col 3: Invalid delimiter ''' after identifier 'a']`

### 5.24 comment markers inside string

```
"#/ not a comment /#";
```

**Expected:** ✅ no errors — tokens: LIT_INSCRIPTION RS_TERMINATOR

## 6. Comments

### 6.1 simple

```
#/ hi /#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.2 empty #//#

```
#//#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.3 #///#

```
#///#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.4 slashes inside

```
#/ a / b // c /#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.5 hash inside

```
#/ a # b /#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.6 multiline

```
#/ line1
line2
line3 /#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.7 comment then code

```
#/ c /# aether x;
```

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_TERMINATOR

### 6.8 code then comment

```
x; #/ c /#
```

**Expected:** ✅ no errors — tokens: IDENTIFIER RS_TERMINATOR

### 6.9 two comments

```
#/ a /# #/ b /#
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 6.10 unterminated

```
#/ never closed
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated comment: '#/ never closed']`

### 6.11 only '#/'

```
#/
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated comment: '#/']`

### 6.12 ends with '/' no '#'

```
#/ abc /
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated comment: '#/ abc /']`

### 6.13 lone '#'

```
# x
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '#']`
- tokens still produced: IDENTIFIER

### 6.14 non-ASCII in comment

```
#/ café /#
```

⚠ Exact input: `'#/ café /#'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 7: Invalid character 'é' in comment]`

### 6.16 comment glued to next token

```
#/ c /#x
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 8: Invalid delimiter 'x' after comment]`
- tokens still produced: IDENTIFIER

### 6.17 comment glued to ';'

```
#/ c /#;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 8: Invalid delimiter ';' after comment]`
- tokens still produced: RS_TERMINATOR

## 7. Operators & symbols

### 7.1 all compound assigns

```
x += 1; x -= 1; x *= 1; x /= 1; x %= 1;
```

**Expected:** ✅ no errors — tokens: IDENTIFIER RS_ADD_ASSIGN AETHER_LITERAL RS_TERMINATOR IDENTIFIER RS_SUB_ASSIGN AETHER_LITERAL RS_TERMINATOR IDENTIFIER RS_MULTIPLY_ASSIGN AETHER_LITERAL RS_TERMINATOR IDENTIFIER RS_DIVIDE_ASSIGN …

### 7.2 increment/decrement

```
x++; x--;
```

**Expected:** ✅ no errors — tokens: IDENTIFIER RS_INCREMENT RS_TERMINATOR IDENTIFIER RS_DECREMENT RS_TERMINATOR

### 7.3 relational

```
x < y; x > y; x <= y; x >= y; x == y; x != y;
```

**Expected:** ✅ no errors — tokens: IDENTIFIER RS_LESS_THAN IDENTIFIER RS_TERMINATOR IDENTIFIER RS_GREATER_THAN IDENTIFIER RS_TERMINATOR IDENTIFIER RS_LESS_THAN_EQUAL IDENTIFIER RS_TERMINATOR IDENTIFIER RS_GREATER_THAN_EQUAL …

### 7.4 logical

```
x && y; x || y; !x;
```

**Expected:** ✅ no errors — tokens: IDENTIFIER RS_AND IDENTIFIER RS_TERMINATOR IDENTIFIER RS_OR IDENTIFIER RS_TERMINATOR RS_NOT IDENTIFIER RS_TERMINATOR

### 7.5 single & (invalid)

```
x & y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Unexpected character ' ' after '&'. Expected '&&']`
- tokens still produced: IDENTIFIER IDENTIFIER

### 7.6 single | (invalid)

```
x | y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Unexpected character ' ' after '|'. Expected '||']`
- tokens still produced: IDENTIFIER IDENTIFIER

### 7.7 triple ===

```
x === y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 5: Invalid delimiter '=' after '==']`
- tokens still produced: IDENTIFIER RS_ASSIGN IDENTIFIER

### 7.8 => (invalid)

```
x => y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '>' after '=']`
- tokens still produced: IDENTIFIER RS_GREATER_THAN IDENTIFIER

### 7.9 << (invalid)

```
x << y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '<' after '<']`
- tokens still produced: IDENTIFIER RS_LESS_THAN IDENTIFIER

### 7.10 x+++y

```
x+++y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter '+' after '++']`
- tokens still produced: IDENTIFIER RS_ADD IDENTIFIER

### 7.11 pre-increment ++x

```
++x
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter 'x' after '++']`
- tokens still produced: IDENTIFIER

### 7.12 unary minus -x (use ~)

```
f(-x)
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter '-' after '(']`
- tokens still produced: IDENTIFIER RS_MINUS IDENTIFIER RS_CLOSE_PARENTHESIS

### 7.13 tilde negation ~x

```
~x
```

**Expected:** ✅ no errors — tokens: RS_NEGATIVE IDENTIFIER

### 7.14 tilde paren ~(x)

```
~(x)
```

**Expected:** ✅ no errors — tokens: RS_NEGATIVE RS_OPEN_PARENTHESIS IDENTIFIER RS_CLOSE_PARENTHESIS

### 7.15 double bang !!x

```
!!x
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter '!' after '!']`
- tokens still produced: RS_NOT IDENTIFIER

### 7.16 dot access a.b

```
a.b
```

**Expected:** ✅ no errors — tokens: IDENTIFIER RS_DOT IDENTIFIER

### 7.17 dot then space a. b

```
a. b
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter ' ' after '.']`
- tokens still produced: IDENTIFIER IDENTIFIER

### 7.18 dot then digit a.1

```
a.1
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter '1' after '.']`
- tokens still produced: IDENTIFIER AETHER_LITERAL

### 7.19 double dot a..b

```
a..b
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter '.' after '.']`
- tokens still produced: IDENTIFIER RS_DOT IDENTIFIER

### 7.20 double semicolon

```
;;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter ';' after ';']`
- tokens still produced: RS_TERMINATOR

### 7.21 double comma

```
x,,y
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter ',' after ',']`
- tokens still produced: IDENTIFIER RS_COMMA IDENTIFIER

### 7.22 empty parens

```
()
```

**Expected:** ✅ no errors — tokens: RS_OPEN_PARENTHESIS RS_CLOSE_PARENTHESIS

### 7.23 empty brackets []

```
[]
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter ']' after '[']`
- tokens still produced: RS_CLOSE_BRACKET

### 7.24 empty braces {}

```
{}
```

**Expected:** ✅ no errors — tokens: RS_OPEN_CURLY_BRACE RS_CLOSE_CURLY_BRACE

### 7.25 deep nesting (200 parens)

```
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((x))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
```

**Expected:** ✅ no errors — tokens: RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS RS_OPEN_PARENTHESIS …

### 7.26 unknown chars

```
@
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '@']`

### 7.27 dollar

```
$
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '$']`

### 7.28 backtick

```
`
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '`']`

### 7.29 caret

```
^
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '^']`

### 7.30 question mark

```
?
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '?']`

### 7.31 colon

```
:
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character ':']`

### 7.32 backslash outside string

```
\
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '\\']`

### 7.33 non-ASCII outside string

```
é
```

⚠ Exact input: `'é'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character 'é']`

### 7.34 vertical tab / form feed

```

```

⚠ Exact input: `'\x0b'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '\x0b']`

### 7.35 non-breaking space

```
 
```

⚠ Exact input: `'\xa0'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '\xa0']`

## 8. Whitespace & EOF

### 8.1 empty file

```
(empty file)
```

**Expected:** ✅ no errors — tokens: (no tokens)

### 8.2 only spaces

```
     
```

⚠ Exact input: `'     '`

**Expected:** ✅ no errors — tokens: (no tokens)

### 8.3 only newlines

```




```

⚠ Exact input: `'\n\n\n'`

**Expected:** ✅ no errors — tokens: (no tokens)

### 8.4 CRLF line endings

```
aether x;
aether y;

```

⚠ Exact input: `'aether x;\r\naether y;\r\n'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_TERMINATOR RW_AETHER IDENTIFIER RS_TERMINATOR

### 8.5 lone CR line endings

```
aether x;
aether y;
```

⚠ Exact input: `'aether x;\raether y;\r'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_TERMINATOR RW_AETHER IDENTIFIER RS_TERMINATOR

### 8.6 tabs everywhere

```
	aether	x	=	5	;	
```

⚠ Exact input: `'\taether\tx\t=\t5\t;\t'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_ASSIGN AETHER_LITERAL RS_TERMINATOR

### 8.7 no trailing newline

```
aether x = 5;
```

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_ASSIGN AETHER_LITERAL RS_TERMINATOR

### 8.10 ends right after '('

```
f(
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter 'None' after '(']`
- tokens still produced: IDENTIFIER

### 8.11 ends right after '{'

```
{
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter 'None' after '{']`

### 8.12 ends right after '='

```
x =
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid delimiter 'None' after '=']`
- tokens still produced: IDENTIFIER

### 8.13 ends right after ','

```
x,
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Invalid delimiter 'None' after ',']`
- tokens still produced: IDENTIFIER

### 8.14 ends right after '&'

```
x &
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Unexpected character 'None' after '&'. Expected '&&']`
- tokens still produced: IDENTIFIER

### 8.15 ends inside number 1.

```
1.
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 3: Expected a digit after '.' in '1.']`

### 8.16 ends after '~'

```
~
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 2: Invalid delimiter 'None' after '~']`

## 9. Error recovery

### 9.1 two bad chars, good code between

```
@ aether x; $
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '@']`
- `Lexical Error [Line 1, Col 13: Unexpected symbol character '$']`
- tokens still produced: RW_AETHER IDENTIFIER RS_TERMINATOR

### 9.2 bad number then valid code

```
01; aether x;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Leading zeros are not allowed ('01')]`
- tokens still produced: RS_TERMINATOR RW_AETHER IDENTIFIER RS_TERMINATOR

### 9.3 bad string then valid code

```
"abc
aether x;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unterminated inscription literal: '"abc']`
- tokens still produced: RW_AETHER IDENTIFIER RS_TERMINATOR

### 9.4 bad escape keeps reading string

```
"a\qb" aether x;
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid escape sequence '\q']`
- tokens still produced: RW_AETHER IDENTIFIER RS_TERMINATOR

### 9.5 error inside comment doesn't kill rest

```
#/ é /# aether x;
```

⚠ Exact input: `'#/ é /# aether x;'`

**Expected:** ❌
- `Lexical Error [Line 1, Col 4: Invalid character 'é' in comment]`
- tokens still produced: RW_AETHER IDENTIFIER RS_TERMINATOR

### 9.6 many errors in a row

```
@ $ ^ ? : ` \
```

**Expected:** ❌
- `Lexical Error [Line 1, Col 1: Unexpected symbol character '@']`
- `Lexical Error [Line 1, Col 3: Unexpected symbol character '$']`
- `Lexical Error [Line 1, Col 5: Unexpected symbol character '^']`
- `Lexical Error [Line 1, Col 7: Unexpected symbol character '?']`
- `Lexical Error [Line 1, Col 9: Unexpected symbol character ':']`
- `Lexical Error [Line 1, Col 11: Unexpected symbol character '`']`
- `Lexical Error [Line 1, Col 13: Unexpected symbol character '\\']`

## 10. Realistic programs

### 10.1 declarations

```
aether x = 5;
essence y = 2.5;
inscription s = "hi";
aura a = blessed;

```

⚠ Exact input: `'aether x = 5;\nessence y = 2.5;\ninscription s = "hi";\naura a = blessed;\n'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_ASSIGN AETHER_LITERAL RS_TERMINATOR RW_ESSENCE IDENTIFIER RS_ASSIGN ESSENCE_LITERAL RS_TERMINATOR RW_INSCRIPTION IDENTIFIER RS_ASSIGN LIT_INSCRIPTION …

### 10.2 arithmetic

```
aether x = (a + b) * ~c / d % 2;

```

⚠ Exact input: `'aether x = (a + b) * ~c / d % 2;\n'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_ASSIGN RS_OPEN_PARENTHESIS IDENTIFIER RS_ADD IDENTIFIER RS_CLOSE_PARENTHESIS RS_MULTIPLY RS_NEGATIVE IDENTIFIER RS_DIVIDE IDENTIFIER RS_MODULO …

### 10.3 condition

```
chant (x >= 5 && !done) {
    x++;
}

```

⚠ Exact input: `'chant (x >= 5 && !done) {\n    x++;\n}\n'`

**Expected:** ✅ no errors — tokens: RW_CHANT RS_OPEN_PARENTHESIS IDENTIFIER RS_GREATER_THAN_EQUAL AETHER_LITERAL RS_AND RS_NOT IDENTIFIER RS_CLOSE_PARENTHESIS RS_OPEN_CURLY_BRACE IDENTIFIER RS_INCREMENT RS_TERMINATOR RS_CLOSE_CURLY_BRACE

### 10.4 comments between code

```
aether x = 5; #/ five /#
aether y = 6; #/ six /#

```

⚠ Exact input: `'aether x = 5; #/ five /#\naether y = 6; #/ six /#\n'`

**Expected:** ✅ no errors — tokens: RW_AETHER IDENTIFIER RS_ASSIGN AETHER_LITERAL RS_TERMINATOR RW_AETHER IDENTIFIER RS_ASSIGN AETHER_LITERAL RS_TERMINATOR

### 10.5 function call args

```
summon f(1, 2.5, "a", ~3);

```

⚠ Exact input: `'summon f(1, 2.5, "a", ~3);\n'`

**Expected:** ✅ no errors — tokens: RW_SUMMON IDENTIFIER RS_OPEN_PARENTHESIS AETHER_LITERAL RS_COMMA ESSENCE_LITERAL RS_COMMA LIT_INSCRIPTION RS_COMMA AETHER_LITERAL RS_CLOSE_PARENTHESIS RS_TERMINATOR

## 11. KNOWN HOLES

### 11.1 brace on its own line (fallback\n{)

```
fallback
{
}
```

**Expected (desired):** 🕳️ no errors — tokens: RW_FALLBACK RS_OPEN_CURLY_BRACE RS_CLOSE_CURLY_BRACE
**Currently:** ❌ `Lexical Error [Line 1, Col 9: Invalid delimiter '\n' after keyword 'fallback']`

### 11.2 brace on its own line (invoke\n{)

```
invoke
{
}
```

**Expected (desired):** 🕳️ no errors — tokens: RW_INVOKE RS_OPEN_CURLY_BRACE RS_CLOSE_CURLY_BRACE
**Currently:** ❌ `Lexical Error [Line 1, Col 7: Invalid delimiter '\n' after keyword 'invoke']`

### 11.3 newline after keyword (aether\nx)

```
aether
x;
```

**Expected (desired):** 🕳️ no errors — tokens: RW_AETHER IDENTIFIER RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 7: Invalid delimiter '\n' after keyword 'aether']`

### 11.4 newline after null

```
x = null
;
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_ASSIGN RW_NULL RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 9: Invalid delimiter '\n' after keyword 'null']`

### 11.5 wrapped call args f(\n1)

```
f(
1)
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_OPEN_PARENTHESIS AETHER_LITERAL RS_CLOSE_PARENTHESIS
**Currently:** ❌ `Lexical Error [Line 1, Col 3: Invalid delimiter '\n' after '(']`

### 11.6 wrapped assignment x =\n5

```
x =
5;
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_ASSIGN AETHER_LITERAL RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 4: Invalid delimiter '\n' after '=']`

### 11.7 wrapped expression x +\ny

```
x +
y;
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_ADD IDENTIFIER RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 4: Invalid delimiter '\n' after '+']`

### 11.8 wrapped logic x &&\ny

```
x &&
y;
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_AND IDENTIFIER RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 5: Invalid delimiter '\n' after '&&']`

### 11.9 null in brackets [null]

```
[null]
```

**Expected (desired):** 🕳️ no errors — tokens: RS_OPEN_BRACKET RW_NULL RS_CLOSE_BRACKET
**Currently:** ❌ `Lexical Error [Line 1, Col 6: Invalid delimiter ']' after keyword 'null']`

### 11.10 null!=x

```
null!=x
```

**Expected (desired):** 🕳️ no errors — tokens: RW_NULL RS_NOT_EQUAL IDENTIFIER
**Currently:** ❌ `Lexical Error [Line 1, Col 5: Invalid delimiter '!' after keyword 'null']`

### 11.11 essence in index x[1.5]

```
x[1.5]
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_OPEN_BRACKET ESSENCE_LITERAL RS_CLOSE_BRACKET
**Currently:** ❌ `Lexical Error [Line 1, Col 6: Invalid delimiter ']' after essence literal '1.5']`

### 11.12 comment right after ';'

```
x;#/ c /#
```

**Expected (desired):** 🕳️ no errors — tokens: IDENTIFIER RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 3: Invalid delimiter '#' after ';']`

### 11.13 comment right after number

```
5#/ c /#
```

**Expected (desired):** 🕳️ no errors — tokens: AETHER_LITERAL
**Currently:** ❌ `Lexical Error [Line 1, Col 2: Invalid delimiter '#' after aether literal '5']`

### 11.14 comment followed by ';'

```
#/ c /#;
```

**Expected (desired):** 🕳️ no errors — tokens: RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 8: Invalid delimiter ';' after comment]`

### 11.15 char literal 'a'

```
'a'
```

**Expected (desired):** 🕳️ no errors — tokens: LIT_GLYPH
**Currently:** ❌ `Lexical Error [Line 1, Col 1: Unexpected symbol character "'"]` | `Lexical Error [Line 1, Col 3: Invalid delimiter ''' after identifier 'a']`

### 11.16 unterminated string causes only ONE error

```
"hi
"
```

**Expected (desired):** 🕳️ exactly 1 error
**Currently:** ❌ `Lexical Error [Line 1, Col 1: Unterminated inscription literal: '"hi']` | `Lexical Error [Line 2, Col 1: Unterminated inscription literal: '"']`

### 11.17 conjure should be a keyword (if still in the language)

```
conjure x
```

**Expected (desired):** 🕳️ no errors — tokens: RW_CONJURE IDENTIFIER
**Currently:** ✅ tokens: IDENTIFIER IDENTIFIER

### 11.18 17-digit number leaves no stray token

```
12345678901234567;
```

**Expected (desired):** 🕳️ an error containing “invalid delimiter” and ONLY these tokens: RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 17: '1234567890123456' has invalid delimiter '7']`

### 11.19 9-frac-digit number leaves no stray token

```
1.123456789;
```

**Expected (desired):** 🕳️ an error containing “invalid delimiter” and ONLY these tokens: RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 11: '1.12345678' has invalid delimiter '9']`

### 11.20 5.5.5 leaves no stray token

```
5.5.5;
```

**Expected (desired):** 🕳️ an error containing “Invalid delimiter '.'” and ONLY these tokens: RS_TERMINATOR
**Currently:** ❌ `Lexical Error [Line 1, Col 4: Invalid delimiter '.' after essence literal '5.5']` | `Lexical Error [Line 1, Col 5: Invalid delimiter '5' after '.']`

## Stress tests (too long to paste — generate the input)

Run in Python, copy the output, paste into the UI:

### very long string (5000 chars)
```python
print('"' + "a"*5000 + '";')
```
**Expected:** ✅ no errors — LIT_INSCRIPTION, RS_TERMINATOR

### very long comment (20000 chars)
```python
print('#/' + "a"*20000 + '/#')
```
**Expected:** ✅ no errors, no tokens

### very long line (10000 tokens)
```python
print('x + '*10000 + 'x')
```
**Expected:** ✅ no errors, 20001 tokens

### many lines (5000)
```python
print('aether x = 5;\n'*5000)
```
**Expected:** ✅ no errors, 25000 tokens; last token on line 5000
