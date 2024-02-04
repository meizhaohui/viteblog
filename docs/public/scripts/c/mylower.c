/* filename: mylower.c */
#include <ctype.h>
#include <stdio.h>

int main( )
{
    int c;

    // 不断从标准输入读入字符
    while ((c = getchar( )) != EOF)
        // 输出小写的字符
        putchar(tolower(c));

    return 0;
}
