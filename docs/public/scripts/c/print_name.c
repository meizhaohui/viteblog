/* filename: print_name.c */

#include <stdio.h>

#define N 100

// 函数声明
int change_name(char string[]);

// 函数定义
int change_name(char string[N])
{
    for (int i = 0; string[i] != '\0'; i++) {
        if ('A' <= string[i] && 'Z' >= string[i]) {
            string[i] += 32;
        } else if ('a' <= string[i] && 'z' >= string[i]) {
            string[i] -= 32;
        }
    }
    for (int i = 0; string[i] != '\0'; i++) {
        printf("%c", string[i]);
    }
    printf("\n");
    return 0;
}

// 主函数
int main(int argc, char *argv[])
{
    change_name(argv[0]);

    return 0;
}
