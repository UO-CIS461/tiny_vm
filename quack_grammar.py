
calc_grammar = """
    ?start: program -> end

    ?program: statement*

    statement: soloexpr ";" 
      | assignment ";" 
      | if_block elif_block* [else_block] -> if_handler
      | "while"  rexpr  statement_block -> while_handler
    
    if_block: "if"  rexpr  statement_block
    elif_block: "elif"  rexpr  statement_block
    else_block: "else" statement_block

    ?statement_block: "{" statement* "}"

    assignment: lexpr ":" type "=" rexpr -> assign
              | lexpr "=" rexpr -> assign_infertype

    ?soloexpr: rexpr -> solo_statement

    ?type: NAME

    ?lexpr: NAME

    ?rexpr: rexpr1
            | condition
    
    ?rexpr1: rexpr2
            | "not" rexpr1      -> _not
            | relation

    ?rexpr2:"(" rexpr ")"
            | methodcall
            | atom
            | rexpr2 "*" rexpr2  -> mul
            | rexpr2 "/" rexpr2 -> div
            | rexpr2 "+" rexpr2  -> add
            | rexpr2 "-" rexpr2  -> sub



    

    ?methodcall: rexpr2 "." methodname "(" methodargs ")" -> methodcall
    
    ?methodname : NAME
    ?methodargs: (rexpr ("," rexpr)* )? -> methodargs          


    ?atom: INT           -> const_number
         | "-" rexpr2         -> neg
         | lexpr            -> var
         | "true" -> const_true
         | "false" -> const_false
         | "nothing" -> const_nothing
         | string -> const_string

    ?condition:   rexpr1 "and" rexpr1 -> _and
                | rexpr1 "or" rexpr1 -> _or

    
    ?relation:  rexpr2 "<" rexpr2 -> less
              | rexpr2 "<=" rexpr2 -> atmost
              | rexpr2 ">" rexpr2 -> more
              | rexpr2 ">=" rexpr2 -> atleast
              | rexpr2 "==" rexpr2 -> equals
    
    ?string: ESCAPED_STRING

    %import common.CNAME -> NAME
    %import common.INT
    %import common.ESCAPED_STRING
    %import common.CPP_COMMENT 

    %import common.WS_INLINE
    %import common.WS

    %ignore WS_INLINE
    %ignore WS
    %ignore CPP_COMMENT
"""

clsnames = ['Obj', 'Int', 'Bool', 'String', 'Nothing']
clsname_hierarchy = {i: 'Obj' for i in clsnames}
relational_methods = {'less', 'more', 'equals', 'atmost', 'atleast'}
nothing_methods = {'print'}
str_methods = {'string'}
arithmetic_methods = {'mul', 'sub', 'div', 'neg', 'plus'}
logical_methods = {'not'}
OBJ_methods = {'print', 'equals', 'string'}
STRING_methods = OBJ_methods | {'plus'} | relational_methods
INT_methods = OBJ_methods | arithmetic_methods | relational_methods
BOOL_methods = OBJ_methods | logical_methods
NOTHING_methods = OBJ_methods
methodlist = {}
for cls, methods in zip(clsnames, [OBJ_methods, INT_methods, BOOL_methods, STRING_methods, NOTHING_methods]):
    methodlist[cls] = {}
    temp = methodlist[cls]
    for method in methods:
        if method in relational_methods:
            temp[method] = [[cls], 'Bool']
        elif method in nothing_methods:
            temp[method] = [[], 'Nothing']
        elif method in arithmetic_methods:
            temp[method] = [[cls], cls]
        elif method in logical_methods:
            temp[method] = [[], 'Bool']
        elif method in str_methods:
            temp[method] = [[], 'String']
def commontype(t1,t2):
    if t1 == t2:
        return t1
    t1p= clsname_hierarchy[t1]
    t2p= clsname_hierarchy[t2]
    if t1 == t2p:
        return t1p
    if t2 == t1p:
        return t2
    return commontype(t1p,t2p)
