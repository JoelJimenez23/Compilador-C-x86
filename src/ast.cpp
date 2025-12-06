#include "ast.h"

Exp::~Exp() {}



string Exp::binopToChar(BinaryOp op) {
    switch (op) {
        case PLUS_OP:  return "+";
        case MINUS_OP: return "-";
        case MUL_OP:   return "*";
        case DIV_OP:   return "/";
        case POW_OP:   return "**";
        case LE_OP:    return "<";
        case GT_OP:    return ">";
        case EQUAL_OP: return "==";
        case NEQUAL_OP: return "!=";
        default:       return "?";

    }

}





// ------------------ BinaryExp ------------------
// BinaryExp::BinaryExp(Exp* l, Exp* r, BinaryOp o)
//     : left(l), right(r), op(o) {}
BinaryExp::BinaryExp(Exp* l, Exp* r, BinaryOp o) {
    left  = l;
    right = r;
    op    = o;

    hoja     = false;
    etiqueta = 1 + std::max(left->etiqueta, right->etiqueta);

    isnumber = false;
    valor    = 0;

    if (left->isnumber && right->isnumber) {
        isnumber = true;

        switch (op) {
            case PLUS_OP:
                valor = left->valor + right->valor;
                break;
            case MINUS_OP:
                valor = left->valor - right->valor;
                break;
            case MUL_OP:
                valor = left->valor * right->valor;
                break;
            case LE_OP:
                valor = (left->valor <= right->valor) ? 1 : 0;
                break;
            case GT_OP:
                valor = (left->valor > right->valor) ? 1 : 0;
                break;
            case EQUAL_OP:
                valor = (left->valor == right->valor) ? 1 : 0;
                break;
            case NEQUAL_OP:
                valor = (left->valor != right->valor) ? 1 : 0;
                break;
            // si tienes más operadores, agrégalos acá
            default:
                isnumber = false;  // por si hay alguno que no quieras foldar
                break;
        }
    }
}



BinaryExp::~BinaryExp() {
    delete left;
    delete right;
}

// ------------------ NumberExp ------------------
NumberExp::NumberExp(int v) : value(v) {
    value    = v;
    hoja     = true;
    isnumber = true;
    valor    = v;
    etiqueta = 1;
}

NumberExp::~NumberExp() {}

// ------------------ IdExp ------------------
IdExp::IdExp(string v) : value(v) {}

IdExp::~IdExp() {}


StringExp::StringExp(string v) : value(v) {}
StringExp::~StringExp() {}
