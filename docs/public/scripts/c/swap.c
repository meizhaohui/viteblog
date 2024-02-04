#include <stdio.h>

int oldswap(int x, int y);
int swap(int *px, int *py);


int main( )
{
    int a = 1;
    int b = 2;
    printf("原始值:\t\t\ta = %d, b = %d\n", a, b);
    oldswap(a, b);
    printf("使用oldswap交换后:\ta = %d, b = %d\n", a, b);
    // 主调程序将指向所要交换的变量的指针传递给被调用函数
    // &a 表示指向变量a的指针
    // &b 表示指向变量b的指针
    swap(&a, &b);
    printf("使用swap交换后:\t\ta = %d, b = %d\n", a, b);

    return 0;
}

int oldswap(int x, int y)
{
    int temp;

    temp = x;
    x    = y;
    y    = temp;

    return 0;
}

// swap函数的所有参数都声明为指针
// 通过这种指针来间接访问它们指向的操作数
// 指针参数使得被调用函数能够访问和修改主调函数中对象的值
int swap(int *px, int *py)
{
    int temp;

    temp = *px;
    *px  = *py;
    *py  = temp;

    return 0;
}