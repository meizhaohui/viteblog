/* filename: use_variable_length_parameter.c */

// stdarg.h头文件包含一组宏定义，它们对如何遍历参数表进行了定义
#include <stdarg.h>
#include <stdio.h>

// 省略号...表示参数表参数的数量和类型是可变的。
// 省略号...只能出现在参数表的尾部
void print_values(int count, ...)
{
    // va_list类型用于声明一个变量，该变量将依次引用各参数
    // args意思是参数指针
    va_list args;
    // 宏va_start将args初始化为指向第一个无名参数的指针
    // 在使用args之前，必须调用一次va_start宏
    va_start(args, count);
    for (int i = 0; i < count; i++) {
        // 每次调用va_arg，该函数都将返回一个参数，并将args指向下一个参数
        // va_arg使用一个类型名来决定返回的对象类型，指针移动的步长
        printf("%d ", va_arg(args, int));
    }
    printf("\n");
    // 最后，必须在函数返回之前调用va_end，以完成一些必要的清理工作
    va_end(args);
}

int main(int argc, char *argv[])
{
    print_values(3, 1, 2, 3);          // 输出 "1 2 3"
    print_values(5, 1, 2, 3, 4, 5);    // 输出 "1 2 3 4 5"

    return 0;
}
