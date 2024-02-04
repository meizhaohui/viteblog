/**
*@file count_digit_and_space.c
*@brief 使用switch语句统计各个数字、空白字符及其他所有字符出现的次数
*@author Zhaohui Mei<mzh.whut@gmail.com>
*@date 2019-11-10
*@return 0
*/

#include <stdio.h>


// 函数声明
int count_digit_space(void);

// 函数定义
int count_digit_space(void)
{
    int c, i, nwhite, nother, ndigit[10];
    
    nwhite = nother = 0;
    for (i = 0; i<10; i++)
       ndigit[i] = 0;
    while ((c = getchar()) != EOF)
    {
        switch (c) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                printf("case %c\n", c);
                ndigit[c - '0']++;
                break;
            case ' ':
            case '\t':
            case '\n':
                printf("case space/tab/new_line\n");
                nwhite++;
                break;
            default:
                printf("case default\n");
                nother++;
                break;
       }
    }
   
    printf("digits =");
    for (i=0; i<10; i++){
        printf(" %d", ndigit[i]);
    }
    printf(", white space = %d, other = %d\n", nwhite, nother);
    return 0;
}

// 主函数
int main(int argc, char *argv[])
{
    count_digit_space();
    return 0;
}
