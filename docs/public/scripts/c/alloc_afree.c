#include <stdio.h>
#define ALLOCSIZE 8 /* 可用空间大小 */

// 静态字符数组，对外不可见
static char allocbuf[ALLOCSIZE]; /* alloc使用的存储区 */
// allocp指针指向allocbuf下一个
static char *allocp = allocbuf; /* 下一个空间位置 */

char *allac(int n) /* 返回指向n个字符的指针 */
{
    printf("执行函数allac(%d): ", n);
    if (allocbuf + ALLOCSIZE - allocp >= n) { /* 有足够多的空闲空间 */
        allocp += n;
        printf("本次占用空间数: %d, 可用空闲空间数: %ld\n", n, allocbuf + ALLOCSIZE - allocp);
        return allocp - n;
    } else /* 空闲空间不够 */
    {
        printf("可用空闲空间数: %ld，需要分配空闲空间数: %d,空闲空间不足，请先释放\n",
               allocbuf + ALLOCSIZE - allocp, n);

        return 0;
    }
}

void afree(char *p) /* 释放p指向在存储区 */
{
    printf("执行函数afree");
    if (p >= allocbuf && p < allocbuf + ALLOCSIZE) {
        allocp = p;
        printf("释放后，可用空闲空间数:%ld\n", allocbuf + ALLOCSIZE - allocp);
    }
}

int main( )
{
    printf("调用allac和afree函数！\n");

    // 总空闲空间数是8，指针p1分配1个空间，则空闲空间数为7
    char *p1 = allac(1);
    // 总空闲空间数是8，指针p1分配1个空间
    // 再为指针p2分配2个空间，则空闲空间数是5
    char *p2 = allac(2);
    // 由于空间空间数是5，此时想为指针p3分配空间，无法分配，因为可以空闲空间数不足
    char *p3 = allac(6);

    // 将指针p2占用空间释放掉，那么可用空闲空间数就是5+2=7
    afree(p2);
    // 再次为p3分配6个空间空间，空闲空间数变成1
    p3 = allac(6);

    return 0;
}