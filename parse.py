#!/usr/bin/env python
import scan
import sys
filein = open(sys.argv[1]).readlines()
a = scan.Scan(filein)
def test():
    global token
    for i in range(100):
        if a.currentToken != "ENDFILE":
            token = a.getToken()
            printToken()
        else:
            break

token = ""

class treeNode():
    def __init__(self):
        self.data = None
        self.child0 = None
        self.child1 = None
        self.child2 = None
        self.sibling = None

class newStmtNode(treeNode):
    def __init__(self, kind):
        treeNode.__init__(self)
        self.nodekind = "StmtK"
        self.stmtkind = kind
        self.lineno = None
        self.attrname = None

class newExpNode(treeNode):
    def __init__(self, kind):
        treeNode.__init__(self)
        self.nodekind = "ExpK"
        self.expkind = kind
        self.lineno = None
        self.attrname = None
        self.attrop = None
        self.attrval = None
        
def syntaxError(message):
    print("\n>>> ");
    print("Syntax error at line %s: %s"%(a.lineno, message))
    Error = "TRUE"

def match(expected):
    global token
    if token == expected:
        token = a.getToken()
    else:
        syntaxError("match unexpected token -> ")
        printToken()
        print("    ")
        
def stmt_sequence():
    global token
    t = statement()
    p = t
    while token != "ENDFILE" and token != "END" and token != "ELSE" and token != "UNTIL":
        match("SEMI")
        q = statement()
        if q != None:
            if t == None:
                t = p = q
            else:
                p.sibling = q
                p = q
    return t


def statement():
    global token
    t = None
    if token == "IF":
        t = if_stmt()
    elif token == "REPEAT":
        t = repeat_stmt()
    elif token == "ID":
        t = assign_stmt()
    elif token == "READ":
        t = read_stmt()
    elif token == "WRITE":
        t = write_stmt()
    else:
        syntaxError("statment unexpected token -> ")
        printToken()
        token = a.getToken()
    return t

def if_stmt():
    global token 
    t = newStmtNode("IfK")
    match("IF")
    if t != None:
        t.child0 = exp()
    match("THEN")
    if t != None:
        t.child1 = stmt_sequence()
    if token == "ELSE":
        match("ELSE")
        if t != None:
            t.child2 = stmt_sequence()
    match("END")
    return t

def repeat_stmt():
    global token 
    t = newStmtNode("RepeatK")
    match("REPEAT")
    if t != None:
        t.child0 = stmt_sequence()
    match("UNTIL")
    if t != None:
        t.child1 = exp()
    return t

def assign_stmt():
    global token
    t = newStmtNode("AssignK")
    if token == "ID" and t != None:
        t.attrname =  a.tokenString
    match("ID")
    match("ASSIGN")
    if t != None:
        t.child0 = exp()
    return t

def read_stmt():
    global token
    t = newStmtNode("ReadK")
    match("READ")
    if token == "ID" and t != None:
        t.attrname = a.tokenString
    match("ID")
    return t

def write_stmt():
    t = newStmtNode("WriteK")
    match("WRITE")
    if t != None:
        t.child0 = exp()
    return t

def exp():
    global token
    t = simple_exp()
    if token == "LT" or token == "EQ":
        p = newExpNode("OpK")
        if p != None:
            p.child0 = t
            p.attrop = token
            t = p
        match(token)
        if t != None:
            t.child1 = simple_exp()
    return t

def simple_exp():
    global token
    t = term()
    while token == "PLUS" or token == "MINUS":
        p = newExpNode("OpK")
        if p != None:
            p.child0 = t
            p.attrop = token
            t = p
            match(token)
            t.child1 = term()

    return t

def term():
    global token
    t = factor()
    while token == "TIMES" or token == "OVER":
        p = newExpNode("OpK")
        if p != None:
            p.child0 = t
            p.attrop = token
            t = p
            match(token)
            p.child1 = factor()

    return t

def factor():
    global token
    t = None
    if token == "NUM":
        t = newExpNode("ConstK")
        if t != None and token == "NUM":
            t.attrval = a.tokenString
        match("NUM")
    elif token == "ID":
        t = newExpNode("IdK")
        if token == "ID" and token != None:
            t.attrname = a.tokenString
        match("ID")
    elif token == "LPAREN":
        match("LPAREN")
        t = exp()
        match("RPAREN")
    else:
        syntaxError("factor unexpected token -> ")
        printToken();
        token = a.getToken()
    return t

def parse():
    global token
    token = a.getToken()
    t = stmt_sequence()
    if token != "ENDFILE":
        syntaxError("Code ends before file\n")
    return t

i = 0
def printTree(tree):
    global i
    space = i*' '
    i += 1
    while tree != None:
        if tree.nodekind == "StmtK":
            if tree.stmtkind == "IfK":
                print(space+"If")
            elif tree.stmtkind == "Repeat":
                print(space+"Repeat")
            elif tree.stmtkind == "AssignK":
                print(space+"Assign to: %s"%tree.attrname)
            elif tree.stmtkind == "ReadK":
                print(space+"Read: %s"%tree.attrname)
            elif tree.stmtkind == "WriteK":
                print(space+"Write")
            else:
                print(space+"Unknow ExpNode kind")
        elif tree.nodekind == "ExpK":
            if tree.expkind == "OpK":
                print(space+"Op: ")
                print(space+tree.attrop)
            elif tree.expkind == "ConstK":
                print(space+"const: %s"%tree.attrval)
            elif tree.expkind == "IdK":
                print(space+"Id: %s"%tree.attrname)
            else:
                print(space+"Unknow ExpNode kind")
        else:
            print(space+"Unknow node kind")
        printTree(tree.child0)
        printTree(tree.child1)
        printTree(tree.child2)
        tree = tree.sibling
    i -= 1    

def printToken():
    global token
    if token in ("IF", "THEN", "ELSE", "END", "REPEAT", "UNTIL", "READ", "WRITE"):
        print("reserved word: %s\n"%a.tokenString)
    elif token == "ASSIGN":
        print(":=\n")
    elif token == "LT":
        print("<\n")
    elif token == "EQ":
        print("=\n")
    elif token == "LPAREN":
        print("(\n")
    elif token == "RPAREN":
        print(")\n")
    elif token == "SEMI":
        print(";\n")
    elif token == "PLUS":
        print("+\n")
    elif token == "MINUS":
        print("=\n")
    elif token == "TIMES":
        print("*\n")
    elif token == "OVER":
        print("/\n")
    elif token == "ENDFILE":
        print("EOF\n")
    elif token == "NUM":
        print("NUM, val= %s\n"%a.tokenString)
    elif token == "ID":
        print("ID, name= %s\n"%a.tokenString)
    elif token == "ERROR":
        print("ERROR: %s\n"%a.tokenString)
    else:
        print("Unknow token: %s\n"%token)
    
def test2():
    global token
    syntaxTree = parse()
    printTree(syntaxTree)


if __name__ == "__main__":
    
    test2()    
    
    
            
    

