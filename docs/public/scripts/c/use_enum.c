/**
*@file use_enum.c
*@brief  使用enum枚举类型 
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-10-21
*@return 0
*/

#include <stdio.h>

enum season {spring, summer, autumn=3, winter};
enum DAY {MON=1, TUE, WED, THU=7, FRI, SAT, SUN};

int main()
{
    printf("spring: %d\n", spring);
    printf("summer: %d\n", summer);
    printf("autumn: %d\n", autumn);
    printf("winter: %d\n", winter);
    printf("DAY枚举常量%d %d %d %d %d %d %d\n", MON, TUE, WED, THU, FRI, SAT, SUN );
}

