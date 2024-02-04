/* filename: year_day.c */
#include <stdio.h>

static char daytab[2][13] = {
    //   1   2   3   4   5   6   7  8   9   10  11  12
    {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31},
    {0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}};

int is_leap(int year) { return year % 4 == 0 && year % 100 != 0 || year % 400 == 0; }
int day_of_year(int year, int month, int day)
{
    int i, leap;
    leap = is_leap(year);

    for (i = 1; i < month; i++)
        day += daytab[leap][i];

    return day;
}

int main( )
{
    printf("2022年1月1日是该年中的第%d天\n", day_of_year(2022, 1, 1));
    printf("2022年6月7日是该年中的第%d天\n", day_of_year(2022, 6, 7));
}
