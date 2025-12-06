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
python3 run_all_inputs.py
```

This command compiles all the inputs in the inputs dir.
After running this command we obtain the input_tokens.txt with all the tokens of the input program and the
input.s assembly x86 file.


If you want to run a specific input you could use the next command.

```sh
./compiler input.txt
```

## 📝 Especificación del Lenguaje Pseudo-C

El compilador soporta un subconjunto simplificado del lenguaje C, con ciertas extensiones. A continuación, se presenta la gramática formal en notación de Backus-Naur (BNF) simplificada, detallando la estructura sintáctica aceptada.

---

##  Language Specifications

| Regla | Descripción |
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

### 2. Tipos y Parámetros

| Regla | Descripción |
| :--- | :--- |
| **`Type`** | `'int' \| 'struct' [ ID ] \| 'string'` |
| **`ParamList`** | `Param { ',' Param }` |
| **`Param`** | `\| 'int' ID [ '[' ']' ] \| 'struct' ID ID \| 'string' ID` |
| **`ArgList`** | `Exp { ',' Exp }` |

### 3. Cuerpo de Función (Body) y Declaraciones Locales

| Regla | Descripción |
| :--- | :--- |
| **`Body`** | `{ LocalDeclaration \| Statement }` |
| **`LocalDeclaration`** | `VarDecLocal \| ArrayDecLocal \| StructDecLocal` |
| **`VarDecLocal`** | `Type ID [ '=' Exp ] ';'` |
| **`ArrayDecLocal`** | `Type ID '[' Exp ']' [ '=' ArrayInit ] ';'` |
| **`StructDecLocal`** | `\| 'struct' ID '{' { StructField } '}'` *(Definición local)* |
| | `\| 'struct' ID ID [ '=' Exp ] ';'` *(Variable local)* |

### 4. Sentencias (Statements)

| Regla | Descripción |
| :--- | :--- |
| **`Statement`** | `AssignStm \| CallStm \| PrintStm \| ReturnStm \| IfStm \| WhileStm` |
| **`AssignStm`** | `\| ID '=' Exp ';'` |
| | `\| ID '[' Exp ']' '=' Exp ';'` *(Asignación en Array)* |
| | `\| ID '.' ID [ '[' Exp ']' ] '=' Exp ';'` *(Asignación en Struct)* |
| **`CallStm`** | `ID '(' [ ArgList ] ')' ';'` |
| **`PrintStm`** | `'print' '(' Exp ')' ';'` |
| **`ReturnStm`** | `'return' Exp ';'` |
| **`IfStm`** | `'if' '(' Exp ')' '{' Body '}' [ 'else' '{' Body '}' ]` |
| **`WhileStm`** | `'while' '(' Exp ')' '{' Body '}'` |

### 5. Expresiones (Expressions) y Jerarquía de Operadores

Las expresiones siguen la jerarquía de operadores estándar, donde `^` (Potencia) tiene la mayor precedencia y `<=` (Comparación) tiene la menor.

| Regla | Precedencia y Operadores |
| :--- | :--- |
| **`Exp`** | `CompExp` |
| **`CompExp`** | `AddExp [ '<=' AddExp ]` *(Comparación)* |
| **`AddExp`** | `MultExp { ( '+' \| '-' ) MultExp }` *(Suma/Resta)* |
| **`MultExp`** | `PowExp { ( '*' \| '/' ) PowExp }` *(Multiplicación/División)* |
| **`PowExp`** | `Factor [ '^' Factor ]` *(Potencia)* |
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
