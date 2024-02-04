/**
*@file print_list_content.c
*@brief print the content of the list
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-11-07
*@return 0
*/

#include <stdio.h>

// 函数声明
int print_list_content(int num);

// 函数定义
int print_list_content(int num)
{
    int list[num];
    for (int i=0; i<num; i++)
    {
        list[i] = i;
    }
    for (int i=0; i<num; i++)
    {
        printf("%6d%c", list[i], (i%10==9 || i==num-1) ? '\n' : ' ');
    }
    return 0;
}

// 主函数
int main()
{
    print_list_content(100);
    return 0;
}

