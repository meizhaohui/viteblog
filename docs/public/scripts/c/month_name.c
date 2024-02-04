/* filename: month_name.c */
#include <stdio.h>
char *month_name(int n);

int main( )
{
    for (int i = 0; i <= 12; i++) {
        char *name;
        name = month_name(i);
        printf("%2d 月对应的英文是 %s\n", i, name);
    }

    return 0;
}

// 返回第n个月份对应的英文名字
char *month_name(int n)
{
    // 定义一个私有的字符串数组
    static char *name[] = {"Illegal month", "January",  "February", "March",  "April",
                           "May",           "June",     "July",     "August", "September",
                           "October",       "November", "December"};

    return (n < 1 || n > 12) ? name[0] : name[n];
}