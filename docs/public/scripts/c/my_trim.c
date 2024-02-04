/**
*@file my_trim.c
*@brief 删除字符串尾部的制表符、空格符和换行符。
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-11-10
*@return 0
*/

#include <stdio.h>
#include <string.h>

// 函数声明
char* my_trim(char s[]);

// 函数定义
char* my_trim(char s[])
{
    int n;
    
    for (n = strlen(s) - 1; n >= 0; n--)
        if (s[n] != ' ' && s[n] != '\t' && s[n] != '\n')
            break;
    s[n+1] = '\0';
    return s;
}

// 主函数
int main(int argc, char *argv[])
{   
    char s1[] = "  hello, world!   	";
    char s2[] = "    -12345		   ";
    printf("'%s' translated to '%s'\n", s1, my_trim(s1));
    printf("'%s' translated to '%s'\n", s2, my_trim(s2));
    return 0;
}
