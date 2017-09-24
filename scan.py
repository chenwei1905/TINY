#!/bin/python

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
        if Scan.lineno != len(self.source) and Scan.linepos == len(Scan.lineBuf):
            Scan.lineno += 1
            Scan.lineBuf = self.source[Scan.lineno-1]
            Scan.linepos = 0
        if Scan.linepos != len(Scan.lineBuf):
            Scan.linepos += 1
            return Scan.lineBuf[Scan.linepos-1]
        if Scan.lineno == len(self.source) and Scan.linepos == len(Scan.lineBuf):
            return -1
    def reservedLookup(self,s):
        if s in Scan.reservedWords.keys():
            return Scan.reservedWords[s]
        return  "ID"

    def ungetNextChar(self):
        Scan.linepos -= 1
        return Scan.lineBuf[Scan.linepos-1]
    
    def getToken(self):
        String = ""
        state = "START"
        while state != "DONE" :
            c = Scan.getNextChar(self)
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
                        Scan.currentToken = "ENDFILE"
                        Scan.tokenno += 1
                    elif c == "=":
                        Scan.currentToken = "EQ"
                        Scan.tokenno += 1
                    elif c == "<":
                        Scan.currentToken = "LT"
                        Scan.tokenno += 1
                    elif c == "+":
                        Scan.currentToken = "PLUS"
                        Scan.tokenno += 1
                    elif c == "-":
                        Scan.currentToken = "MINUS"
                        Scan.tokenno += 1
                    elif c == "*":
                        Scan.currentToken = "TIMES"
                        Scan.tokenno += 1
                    elif c == "/":
                        Scan.currentToken = "OVER"
                        Scan.tokenno += 1
                    elif c == "(":
                        Scan.currentToken = "LPAREN"
                        Scan.tokenno += 1
                    elif c == ")":
                        Scan.currentToken = "PPAREN"
                        Scan.tokenno += 1
                    elif c == ";":
                        Scan.currentToken = "SEMI"
                        Scan.tokenno += 1
                    else:
                        Scan.currentToken = "ERROR"
                        Scan.tokenno += 1
            elif state == "INCOMMENT":
                save = "FALSE"
                if c == "}":
                    state = "START"
            elif state == "INASSIGN":
                state = "DONE"
                if c == "=":
                   Scan.currentToken = "ASSIGN"
                   Scan.tokenno += 1
                else:
                    Scan.ungetNextChar(self)
                    save = "FALSE"
                    Scan.currentToken = "ERROR"
                    Scan.tokenno += 1
            elif state == "INNUM":
                if not str(c).isdigit():
                    Scan.ungetNextChar(self)
                    save = "FALSE"
                    state = "DONE"
                    Scan.currentToken = "NUM"
                    Scan.tokenno += 1
            elif state == "INID":
                if not str(c).isalpha():
                    Scan.ungetNextChar(self)
                    save = "FALSE"
                    state = "DONE"
                    Scan.currentToken = "ID"
                    Scan.tokenno += 1
            elif state == "DONE":
                pass
            else:
                print("Scanner Bug: state = %s\n"%state)
                state = "DONE"
                Scan.currentToken = "ERROR"
                Scan.tokenno += 1
#            print("state:= %s"%state)
#            print("save:= %s"%save)
#            print("char:= %s"%c)
            if state == "DONE":
                Scan.tokenString = String
                String =  ""
                if Scan.currentToken == "ID":
                    Scan.currentToken = Scan.reservedLookup(self,Scan.tokenString)

            if save == "TRUE":
                String = String + c

        return Scan.currentToken        
                    

if __name__ == "__main__":                    
                
    filein = open("test2").readlines()
    a=Scan(filein)
    
    for i in range(100):
        if a.currentToken != "ENDFILE":
            print("token:= %10s, string:= %8s lineno#:= %2s, tokenno:= %2s"%(a.getToken(), a.tokenString, a.lineno, a.tokenno))
        else:
            break


    
        


