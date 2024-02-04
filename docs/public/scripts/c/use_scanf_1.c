/* filename: use_scanf_1.c */

#include <stdio.h>

int main(int argc, char *argv[])
{
    int echo_flag;
    char system_name[50];
    // 数组名本身就是指针，因此system_name前面没有取地址运算符&
    printf("请输入系统名称: ");
    scanf("%s", system_name);
    // 如果要读取包含空格的系统名称，则可以使用以下代码
    // 直到遇到回车键，才读入结束
    // scanf("%[^\n]", system_name);
    printf("请输入打印标志(请输入'1'或'0'，1: 打印输出，0:不打印输出): ");
    scanf("%d", &echo_flag);
    if (echo_flag == 1) {
        printf("打印标志开启，输出系统名称: %s\n", system_name);
    } else {
        printf("打印标志未开启，抱歉，我不知道系统名称!!\n");
    }

    return 0;
}
