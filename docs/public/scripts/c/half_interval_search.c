/**
*@file half_interval_search.c
*@brief half-interval search 折半搜索/二分搜索，查找已经排序的数组v中是否存在某个特定的值x
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-11-09
*@return 0
*/

#include <stdio.h>
#include <stdlib.h>

// 函数声明
int binsearch(int x, int v[], int n);

// 函数定义
int binsearch(int x, int v[], int n)
{
    int low = 0;
    int high = n -1;
    int mid = 0;
    while (low <= high)
    {
        mid = (low + high)/2;
        if (x < v[mid])
        {
            high = mid - 1;
        }
        else if (x > v[mid])
        {
            low = mid + 1;
        }
        else
        {
            return mid; // 找到了匹配的值，返回匹配值的序号
        }
    }
    return -1;  // 没有匹配的值
}

// 主函数
int main(int argc, char *argv[])
{   
    int x = atoi(argv[1]);  // atoi()把字符串转换为一个int整型
    int v[] = {1, 2, 3, 4, 5, 6};
    int n = 6;
    int result = 0;
    result = binsearch(x, v, n);
    printf("Result:%d", result);
    return 0;
}

