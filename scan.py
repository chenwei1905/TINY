#!/usr/bin/env python

class Scan(object):
    StatTpye = ("START", "INASSIGN", "INCOMMENT", "INNUM", "INID", "DONE")
    TokenType = (
        # book-keeping tokens #
        "ENDFILE", "ERROR",
        # reserved words #
        "IF", "THEN", "ELSE", "END", "REPEAT", "UNTIL", "READ", "WRITE",
        # multicharacter tokens #
        "ID", "NUM",
        # special symbols #
        "ASSIGN", "EQ", "LT", "PLUS", "MINUS", "TIMES", "OVER", "LPAREN", "RPAREN", "SEMI"
        )
    reservedWords = {"if":"IF", "then":"THEN", "else":"ELSE", "end":"END", "repeat":"REPEAT", "until":"UNTIL","read":"READ", "write":"WRITE"}    
    
    lineno = 0
    lineBuf =""
    linepos = 0

    currentToken = "" #current token#
    tokenString ="" #save tokenString#
    tokenno =0

    def __init__(self, source):
        self.source = source

    def getNextChar(self):
        if __class__.lineno != len(self.source) and __class__.linepos == len(__class__.lineBuf):
            __class__.lineno += 1
            __class__.lineBuf = self.source[__class__.lineno-1]
            __class__.linepos = 0
        if __class__.linepos != len(__class__.lineBuf):
            __class__.linepos += 1
            return __class__.lineBuf[__class__.linepos-1]
        if __class__.lineno == len(self.source) and __class__.linepos == len(__class__.lineBuf):
            return -1
    def reservedLookup(self,s):
        if s in __class__.reservedWords.keys():
            return __class__.reservedWords[s]
        return  "ID"

    def ungetNextChar(self):
        __class__.linepos -= 1
        return __class__.lineBuf[__class__.linepos-1]
    
    def getToken(self):
        String = ""
        state = "START"
        while state != "DONE" :
            c = __class__.getNextChar(self)
            save = "TRUE"
            if state == "START":
                if str(c).isdigit():
                    state = "INNUM"
                elif str(c).isalpha():
                    state = "INID"
                elif c == ':':
                    state = "INASSIGN"
                elif c == ' ' or c == '\t' or c == '\n':
                    save = "FALSE"
                elif c == '{':
                    save = "FALSE"
                    state = "INCOMMENT"
                else:
                    state = "DONE"
                    if c == -1:
                        save = "FALSE"
                        __class__.currentToken = "ENDFILE"
                        __class__.tokenno += 1
                    elif c == "=":
                        __class__.currentToken = "EQ"
                        __class__.tokenno += 1
                    elif c == "<":
                        __class__.currentToken = "LT"
                        __class__.tokenno += 1
                    elif c == "+":
                        __class__.currentToken = "PLUS"
                        __class__.tokenno += 1
                    elif c == "-":
                        __class__.currentToken = "MINUS"
                        __class__.tokenno += 1
                    elif c == "*":
                        __class__.currentToken = "TIMES"
                        __class__.tokenno += 1
                    elif c == "/":
                        __class__.currentToken = "OVER"
                        __class__.tokenno += 1
                    elif c == "(":
                        __class__.currentToken = "LPAREN"
                        __class__.tokenno += 1
                    elif c == ")":
                        __class__.currentToken = "PPAREN"
                        __class__.tokenno += 1
                    elif c == ";":
                        __class__.currentToken = "SEMI"
                        __class__.tokenno += 1
                    else:
                        __class__.currentToken = "ERROR"
                        __class__.tokenno += 1
            elif state == "INCOMMENT":
                save = "FALSE"
                if c == "}":
                    state = "START"
            elif state == "INASSIGN":
                state = "DONE"
                if c == "=":
                   __class__.currentToken = "ASSIGN"
                   __class__.tokenno += 1
                else:
                    __class__.ungetNextChar(self)
                    save = "FALSE"
                    __class__.currentToken = "ERROR"
                    __class__.tokenno += 1
            elif state == "INNUM":
                if not str(c).isdigit():
                    __class__.ungetNextChar(self)
                    save = "FALSE"
                    state = "DONE"
                    __class__.currentToken = "NUM"
                    __class__.tokenno += 1
            elif state == "INID":
                if not str(c).isalpha():
                    __class__.ungetNextChar(self)
                    save = "FALSE"
                    state = "DONE"
                    __class__.currentToken = "ID"
                    __class__.tokenno += 1
            elif state == "DONE":
                pass
            else:
                print("Scanner Bug: state = %s\n"%state)
                state = "DONE"
                __class__.currentToken = "ERROR"
                __class__.tokenno += 1
#            print("state:= %s"%state)
#            print("save:= %s"%save)
#            print("char:= %s"%c)
            if state == "DONE":
                __class__.tokenString = String
                String =  ""
                if __class__.currentToken == "ID":
                    __class__.currentToken = __class__.reservedLookup(self,__class__.tokenString)

            if save == "TRUE":
                String = String + c

        return __class__.currentToken        
                    

if __name__ == "__main__":                    
                
    filein = open("test2").readlines()
    a=Scan(filein)
    
    for i in range(100):
        if a.currentToken != "ENDFILE":
            print("token:= %10s, string:= %8s lineno#:= %2s, tokenno:= %2s"%(a.getToken(), a.tokenString, a.lineno, a.tokenno))
        else:
            break


    
        


