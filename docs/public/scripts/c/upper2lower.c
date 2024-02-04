/**
*@file upper2lower.c
*@brief translate the UPPER string to lower string
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-11-07
*@return 0
*/

#include <stdio.h>

#define N 100

// 函数声明
int lower(char string[]);

// 函数定义
int lower(char string[N])
{
    for (int i=0; string[i] != '\0'; i++)
    {
        if ('A' <= string[i] && 'Z' >= string[i])
        {
            string[i] += 32;
        }
    }
    for (int i=0; string[i] != '\0'; i++)
    {
        printf("%c", string[i]);
    }
    printf("\n");
    return 0;
}

// 主函数
int main(int argc, char *argv[])
{
    for (int count=0; count < argc; count++)
        lower(argv[count]);
    return 0;
}

