#include "defs.h"
#define extern_
#include "data.h"

#include <stdio.h>
#include <ctype.h>   
#include <string.h>

static int next(void) {
    int c;

    if (Putback) {
        c = Putback;
        Putback = 0;
        return c;
    }

    c = fgetc(Infile);
    if ('\n' == c)
        Line++;
    return c;
};

static void putback(int c) {
    Putback = c;
};

static int skip(void) {
    int c;
    c = next();

    while (' ' == c || '\t' == c || '\n' == c || '\r' == c || '\f' == c) {
        c = next();
    }
    return c;
}

static int chrpos(char *s, int c) {
    char *p;

    p = strchr(s, c);
    return (p ? p -s : -1);
}

static int scanint(int c) {
    int k, val = 0;

    while ((k = chrpos("0123456789", c)) >= 0) {
        val = val * 10 + k;
        c = next();
    };

    putback(c);
    return val;
}

int scan(struct token *t) {
    int c;

    c = skip();

    switch (c) {
    case EOF:
        return (0);
    case '+':
        t->token = T_PLUS;
        break;
    case '-':
        t->token = T_MINUS;
        break;
    case '*':
        t->token = T_MULT;
        break;
    case '/':
        t->token = T_DIV;
        break;
    default:
        if (isdigit(c)) {
            t->intval = scanint(c);
            t->token = T_INTLIT;
            break;
        }

        printf("unrecognized character %c on line %d\n", c, Line);
    }
    return (1);
}

char *tokstr[] = { "+", "-", "*", "/", "intlit"};

static void scanfile() {
    struct token T;

    while (scan(&T)) {
        printf("Token %s", tokstr[T.token]);
        if (T.token == T_INTLIT)
            printf(", value %d", T.intval);
        printf("\n");;
    }
}