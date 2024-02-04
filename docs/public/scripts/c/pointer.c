#include <stdio.h>

int main( )
{
    int c  = 1;
    int *p = &c; /* p是指向int类型的指针，并指向c */
    printf("c = %d\n", c);
    printf("the address c is: %p\n", &p); /* 输出内存地址 */

    return 0;
}
