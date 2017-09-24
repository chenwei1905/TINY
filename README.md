# TINY
一个简单的词法分析和语法分析器

## 词法介绍
```

```
## 语法介绍

## 程序的运行和测试
* 文件 <br>
 ```
 { Sample program
  in TINY language -
  computes factorial
}
read x; { input an integer }
if x < 7+8 then 
   fact := 1;
   repeat 
	fact := fact * x;
	x := x - 1 
   until x = 0;
   wwww := 3
else
   xxxx := 3
end;
x := 1
 ```
* 词法分析的测试结果 <br>

 ```
 token:=       READ, string:=     read lineno#:=  5, tokenno:=  1
token:=         ID, string:=        x lineno#:=  5, tokenno:=  2
token:=       SEMI, string:=          lineno#:=  5, tokenno:=  3
token:=         IF, string:=       if lineno#:=  6, tokenno:=  4
token:=         ID, string:=        x lineno#:=  6, tokenno:=  5
token:=         LT, string:=          lineno#:=  6, tokenno:=  6
token:=        NUM, string:=        7 lineno#:=  6, tokenno:=  7
token:=       PLUS, string:=          lineno#:=  6, tokenno:=  8
token:=        NUM, string:=        8 lineno#:=  6, tokenno:=  9
token:=       THEN, string:=     then lineno#:=  6, tokenno:= 10
token:=         ID, string:=     fact lineno#:=  7, tokenno:= 11
token:=     ASSIGN, string:=        : lineno#:=  7, tokenno:= 12
token:=        NUM, string:=        1 lineno#:=  7, tokenno:= 13
token:=       SEMI, string:=          lineno#:=  7, tokenno:= 14
token:=     REPEAT, string:=   repeat lineno#:=  8, tokenno:= 15
token:=         ID, string:=     fact lineno#:=  9, tokenno:= 16
token:=     ASSIGN, string:=        : lineno#:=  9, tokenno:= 17
token:=         ID, string:=     fact lineno#:=  9, tokenno:= 18
token:=      TIMES, string:=          lineno#:=  9, tokenno:= 19
token:=         ID, string:=        x lineno#:=  9, tokenno:= 20
token:=       SEMI, string:=          lineno#:=  9, tokenno:= 21
token:=         ID, string:=        x lineno#:= 10, tokenno:= 22
token:=     ASSIGN, string:=        : lineno#:= 10, tokenno:= 23
token:=         ID, string:=        x lineno#:= 10, tokenno:= 24
token:=      MINUS, string:=          lineno#:= 10, tokenno:= 25
token:=        NUM, string:=        1 lineno#:= 10, tokenno:= 26
token:=      UNTIL, string:=    until lineno#:= 11, tokenno:= 27
token:=         ID, string:=        x lineno#:= 11, tokenno:= 28
token:=         EQ, string:=          lineno#:= 11, tokenno:= 29
token:=        NUM, string:=        0 lineno#:= 11, tokenno:= 30
token:=       SEMI, string:=          lineno#:= 11, tokenno:= 31
token:=         ID, string:=     wwww lineno#:= 12, tokenno:= 32
token:=     ASSIGN, string:=        : lineno#:= 12, tokenno:= 33
token:=        NUM, string:=        3 lineno#:= 12, tokenno:= 34
token:=       ELSE, string:=     else lineno#:= 13, tokenno:= 35
token:=         ID, string:=     xxxx lineno#:= 14, tokenno:= 36
token:=     ASSIGN, string:=        : lineno#:= 14, tokenno:= 37
token:=        NUM, string:=        3 lineno#:= 14, tokenno:= 38
token:=        END, string:=      end lineno#:= 15, tokenno:= 39
token:=       SEMI, string:=          lineno#:= 15, tokenno:= 40
token:=         ID, string:=        x lineno#:= 16, tokenno:= 41
token:=     ASSIGN, string:=        : lineno#:= 16, tokenno:= 42
token:=        NUM, string:=        1 lineno#:= 16, tokenno:= 43
token:=    ENDFILE, string:=          lineno#:= 16, tokenno:= 44

 ```
 


* 语法分析的测试结果
    * 正确的语法 <br>
```
Read: x
If
 Op: 
 LT
  Id: x
  Op: 
  PLUS
   const: 7
   const: 8
 Assign to: fact
  const: 1
 Unknow ExpNode kind
  Assign to: fact
   Op: 
   TIMES
    Id: fact
    Id: x
  Assign to: x
   Op: 
   MINUS
    Id: x
    const: 1
  Op: 
  EQ
   Id: x
   const: 0
 Assign to: wwww
  const: 3
 Assign to: xxxx
  const: 3
Assign to: x
 const: 1
```
    * 错误的语法 ***缺少if的情况*** <br>
```
>>> 
Syntax error at line 6: match unexpected token -> 
<

    

>>> 
Syntax error at line 6: factor unexpected token -> 
<


>>> 
Syntax error at line 6: match unexpected token -> 
NUM, val= 7

    

>>> 
Syntax error at line 6: statment unexpected token -> 
NUM, val= 7


>>> 
Syntax error at line 6: match unexpected token -> 
+

    

>>> 
Syntax error at line 6: statment unexpected token -> 
+


>>> 
Syntax error at line 6: match unexpected token -> 
NUM, val= 8

    

>>> 
Syntax error at line 6: statment unexpected token -> 
NUM, val= 8


>>> 
Syntax error at line 6: match unexpected token -> 
reserved word: then

    

>>> 
Syntax error at line 6: statment unexpected token -> 
reserved word: then


>>> 
Syntax error at line 7: match unexpected token -> 
ID, name= fact

    

>>> 
Syntax error at line 13: Code ends before file

Read: x
Assign to: x
Assign to: fact
 const: 1
Unknow ExpNode kind
 Assign to: fact
  Op: 
  TIMES
   Id: fact
   Id: x
 Assign to: x
  Op: 
  MINUS
   Id: x
   const: 1
 Op: 
 EQ
  Id: x
  const: 0
Assign to: wwww
 const: 3
```
   
