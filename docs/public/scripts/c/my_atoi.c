/**
*@file my_atoi.c
*@brief 将字符串转换成对应的数值函数atoi,可以处理字符串两端的空格，以前符号位的+/-正负号。
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-11-10
*@return 0
*/

#include <stdio.h>
#include <ctype.h>

// 函数声明
int my_atoi(char s[]);

// 函数定义
int my_atoi(char s[])
{
    int i, n, sign;
    
    for (i = 0; isspace(s[i]); i++)
        ; // 如果是空白符，什么也不做
    
    sign = (s[i] == '-') ? -1 : 1;  // 获取标志位，如果以'-'开头，则是负数，否则是正数
    
    if (s[i] == '+' || s[i] == '-')
        i++;  // 符号位不进行转换，直接跳过
    for (n = 0; isdigit(s[i]); i++)  // 判断字符是否为数字
        n = 10 * n + (s[i] - '0');  // 计算实际的正数值
    return sign * n;  // 返回实际的值
}

// 主函数
int main(int argc, char *argv[])
{   
    char s1[] = "    +12345";
    char s2[] = "    -12345";
    printf("'%s' translated to %d\n", s1, my_atoi(s1));
    printf("'%s' translated to %d\n", s2, my_atoi(s2));
    return 0;
}
