#include <stdio.h>
#include <string.h>

// my_strlen函数返回字符串s的长度
int my_strlen(char *s)
{
    int n;
    // 因为s是一个指针，所以对其执行自增运算是合法的
    // 执行s++运算不会影响到my_strlen函数调用者中的字符串
    // 它仅对该指针在my_strlen函数中的私有副本进行自增运算
    for (n = 0; *s != '\0'; s++)
        n++;
    return n;
}

int main( )
{
    char string[] = "Hello World";
    printf("\"Hello World\"字符串的长度为%d\n", my_strlen(string));
    printf("通过标准库函数strlen获取\"Hello World\"字符串的长度为%lu\n", strlen(string));

    // 定义字符串数组
    char a[20] = {"Hello World!"};
    printf("数组a的长度为%d\n", my_strlen(a));

    // ptr是一个指向char类型对象的指针
    char *ptr = a;
    printf("指针ptr的长度为%d\n", my_strlen(ptr));

    return 0;
}