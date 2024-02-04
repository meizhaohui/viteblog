/* filename: use_scanf.c */

#include <stdio.h>

int main(int argc, char *argv[])
{
    int a, b, c;
    printf("请输入三个数字,两个数字间用空格分隔开: ");
    // &a、&b、&c 中的 & 是地址运算符，分别获得这三个变量的内存地址
    // %d%d%d 是按十进值格式输入三个数值
    // 输入时，在两个数据之间可以用一个或多个空格、tab 键、回车键分隔。我们使用空格分隔
    scanf("%d%d%d", &a, &b, &c);
    printf("你输入的三个数依次是:\n%d\n%d\n%d\n", a, b, c);

    return 0;
}
