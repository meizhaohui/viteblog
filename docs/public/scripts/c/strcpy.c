/* filename: strcpy.c */
#include <stdio.h>

/* 4种不同的实现方法 */
void str_copy1(char *s, char *t);
void str_copy2(char *s, char *t);
void str_copy3(char *s, char *t);
void str_copy4(char *s, char *t);

int main( )
{
    char *message         = "Hello, world";
    char new_message[100] = "Init string";
    printf("%s\n", new_message);
    str_copy4(new_message, message);
    printf("%s\n", new_message);

    return 0;
}

/* 将指针t指向的字符串复制到指针s指向的位置，使用数组下标实现的版本 */
void str_copy1(char *s, char *t)
{
    int i;

    i = 0;
    while ((s[i] = t[i]) != '\0')
        i++;
}

/* 将指针t指向的字符串复制到指针s指向的位置，使用指针方式实现的版本1 */
void str_copy2(char *s, char *t)
{
    while ((*s = *t) != '\0') {
        s++;
        t++;
    }
}

/* 将指针t指向的字符串复制到指针s指向的位置，使用指针方式实现的版本2 */
void str_copy3(char *s, char *t)
{
    /* 将自增运算放到了循环的测试部分中，会先读取数据进行存储，然后再进行自增 */
    while ((*s++ = *t++) != '\0')
        ;
}

/* 将指针t指向的字符串复制到指针s指向的位置，使用指针方式实现的版本3 */
void str_copy4(char *s, char *t)
{
    /* 表达式同'\0'比较是多徐的，只需要判断表达式的值是否为0即可 */
    while ((*s++ = *t++))
        ;
}