/**
*@file base_data_type.c
*@brief 基本数据类型
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-10-20
*@return 0
*/

#include <stdio.h>
#include <limits.h>

int main()
{
    printf("char占用的内存大小是%d\n", sizeof(char));
    printf("short占用的内存大小是%d\n", sizeof(short));
    printf("int占用的内存大小是%d\n", sizeof(int));
    printf("long占用的内存大小是%d\n", sizeof(long));
    printf("float占用的内存大小是%d\n", sizeof(float));
    printf("double占用的内存大小是%d\n", sizeof(double));
    return 0;
}