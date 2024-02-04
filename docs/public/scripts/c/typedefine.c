/* filename: typedefine.c */
#include <stdio.h>

typedef int Length;

int main( )
{
    Length maxlen = 10;
    for (int i = 0; i < maxlen; i++)
        printf("当前是第%d次循环\n", i);
}
