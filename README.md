# C-x86 Compiler
    This repository host a x86 compiler for a subset of C.


## Supported features

* If
* While
* Struct
* Const String
* Arrays
* Reference parameters
* Ternary expressions
* Pseudo print


## Installation

```sh
mkdir build
cd  build
cmake ..
make 
```

After building the project you will have a ./compiler executable.
If you want to compile any file you should the next command.

```sh
./compiler <input_file.txt>
```

## 📝 Especificación del Lenguaje Pseudo-C

The compiler supportws a simplified subset of C. The charts represents the formal grammar in simplified BNF, with the accepted structure.


---

##  Language Specifications

| Rule | Description |
| :--- | :--- |
| **`Program`** | `{ LibraryDecl \| GlobalDeclaration }` |
| **`LibraryDecl`** | `\# 'include' '<' ID '>' ` |
| **`GlobalDeclaration`** | `FunDec \| GlobalVarDec \| StructDec \| ArrayDec` |
| **`FunDec`** | `Type ID '(' [ ParamList ] ')' '{' Body '}'` |
| **`GlobalVarDec`** | `Type ID [ '=' Exp ] ';'` |
| **`StructDec`** | `'struct' ID '{' { StructField } '}' ';'` |
| **`ArrayDec`** | `Type ID '[' Exp ']' [ '=' ArrayInit ] ';'` |
| **`ArrayInit`** | `'{' Exp { ',' Exp } '}'` |
| **`StructField`** | `Type ID [ '[' NUM ']' ] ';'` |

### 2. Types and parameters

| Regla | Descripción |
| :--- | :--- |
| **`Type`** | `'int' \| 'struct' [ ID ] \| 'string'` |
| **`ParamList`** | `Param { ',' Param }` |
| **`Param`** | `\| 'int' ID [ '[' ']' ] \| 'struct' ID ID \| 'string' ID` |
| **`ArgList`** | `Exp { ',' Exp }` |

### 3. Function's body and Local Declaration

| Rule | Description |
| :--- | :--- |
| **`Body`** | `{ LocalDeclaration \| Statement }` |
| **`LocalDeclaration`** | `VarDecLocal \| ArrayDecLocal \| StructDecLocal` |
| **`VarDecLocal`** | `Type ID [ '=' Exp ] ';'` |
| **`ArrayDecLocal`** | `Type ID '[' Exp ']' [ '=' ArrayInit ] ';'` |
| **`StructDecLocal`** | `\| 'struct' ID '{' { StructField } '}'` *(Local definition)* |
| | `\| 'struct' ID ID [ '=' Exp ] ';'` *(Local variable)* |

### 4. Statements

| Regla | Descripción |
| :--- | :--- |
| **`Statement`** | `AssignStm \| CallStm \| PrintStm \| ReturnStm \| IfStm \| WhileStm` |
| **`AssignStm`** | `\| ID '=' Exp ';'` |
| | `\| ID '[' Exp ']' '=' Exp ';'` *(Array assignation)* |
| | `\| ID '.' ID [ '[' Exp ']' ] '=' Exp ';'` *(Struct assignation)* |
| **`CallStm`** | `ID '(' [ ArgList ] ')' ';'` |
| **`PrintStm`** | `'print' '(' Exp ')' ';'` |
| **`ReturnStm`** | `'return' Exp ';'` |
| **`IfStm`** | `'if' '(' Exp ')' '{' Body '}' [ 'else' '{' Body '}' ]` |
| **`WhileStm`** | `'while' '(' Exp ')' '{' Body '}'` |

### 5. Expressions y Operators Hierarchy

The expressions  follow la standard operators hierarchy, where `^` (Pow) has the highest precedence and `<=` (Compare) the least one.

| Regla |  Precedence and Operators |
| :--- | :--- |
| **`Exp`** | `CompExp` |
| **`CompExp`** | `AddExp [ '<=' AddExp ]` *(Compare)* |
| **`AddExp`** | `MultExp { ( '+' \| '-' ) MultExp }` *(Add/Sub)* |
| **`MultExp`** | `PowExp { ( '*' \| '/' ) PowExp }` *(Mul/Div)* |
| **`PowExp`** | `Factor [ '^' Factor ]` *(Pow)* |
| **`Factor`** | `\| NUM` |
| | `\| 'true' \| 'false'` |
| | `\| STRING_LITERAL` |
| | `\| '(' Exp ')'` |
| | `\| FunctionCall` |
| | `\| ArrayAccess` |
| | `\| StructAccess` |
| | `\| ID` |
| **`FunctionCall`** | `ID '(' [ ArgList ] ')'` |
| **`ArrayAccess`** | `ID '[' Exp ']'` |
| **`StructAccess`** | `ID '.' ID [ '[' Exp ']' ]` |
