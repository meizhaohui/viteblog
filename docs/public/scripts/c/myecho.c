/* filename: myecho.c */
#include <stdio.h>

/* 回显命令行参数，版本2 */
int main(int argc, char *argv[])
{
    printf("命令行参数总数argc的值是: %d\n", argc);
    for (int i = 0; i < argc; i++)
        printf("argv[%d]的值是: %s\n", i, argv[i]);

    // argc执行自减运行
    while (--argc > 0) {
        // 因为argv是一个指向参数字符串数组起始位置的指针
        // 所以自增运算++argv将使得它在最开始时指向argv[1]，而不是argv[0]
        // 每执行一次自增运算，就使得argv指向下一个参数，*argv将是指向那个参数的指针
        printf("%s%s", *++argv, (argc > 1) ? " " : "");
    }
    printf("\n");

    return 0;
}