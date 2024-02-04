/* filename: struct_pointer.c */
#include <stdio.h>

// 定义结构体point，表示一个点
struct point {
    int x;    // x是结构的成员，代表横坐标
    int y;    // y也是结构的成员，代表纵坐标
};

int main( )
{
    // 声明一个普通的点结构origin，以及指向点结构对象的指针pp
    struct point origin, *pp;

    // 使用成员运算符对origin点赋值
    origin.x = 1;
    origin.y = 2;

    // 将pp指向origin的地址
    pp = &origin;

    // 访问结构的成员
    printf("origin is (%d, %d)\n", origin.x, origin.y);
    // 结构成员运算符 . 优先级比 * 的优先级高， 因此圆括号是必须的
    // 不能写成 *pp.x，这样是非法的，需要写成 (*pp).x
    printf("origin is (%d, %d)\n", (*pp).x, (*pp).y);

    printf("使用简写p->x形式引用结构成员\n");
    printf("origin is (%d, %d)\n", pp->x, pp->y);

    return 0;
}
