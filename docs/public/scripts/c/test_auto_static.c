/**
*@file test_auto_static.c
*@brief  测试auto自动变量和static静态变量
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-10-21
*@return 0
*/

#include <stdio.h>

void test()
{
    auto int a = 0;
    static int b = 3;
    a++;
    b++;
    printf("a: %d\n", a);
    printf("b: %d\n", b);
}

int main()
{
    for(int i = 0; i < 3; i++)
    {
        test();
    }
    return 0;
}

