#include <stdio.h>

int main( )
{
    // 声明并初始化长度为10的数组a
    int a[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    // 声明指向整型对象的指针
    int *pa;
    // 将指针pa指向数组a的第0个元素
    // pa的值为数组元素a[0]的地址
    pa = &a[0];

    for (int i = 0; i < 10; i++) {
        printf("array item a[%d] = %d address is %p\n", i, a[i], &a[i]);
        // *(pa+i) 则表示数组元素a[i]的内容
        printf("pointer pa + %d value is %p . content is %d\n\n", i, pa + i, *(pa + i));
    }

    return 0;
}