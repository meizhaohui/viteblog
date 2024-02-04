#include <stdio.h>

int main( )
{
    char a_message[] = "array message";     // 定义一个数组
    char *p_message  = "pointer string";    // 定义一个指针
    printf("a_message value is: %s, the address is: %p\n", a_message, &a_message);
    printf("p_message value is: %s, the address is: %p\n", p_message, p_message);
    // 将字符串第一个字母a大写
    a_message[0] = 'A';
    // 指针指向新的其他字符串常量
    p_message = "new pointer message";
    printf("a_message value is: %s, the address is: %p\n", a_message, &a_message);
    printf("p_message value is: %s, the address is: %p\n", p_message, p_message);

    return 0;
}