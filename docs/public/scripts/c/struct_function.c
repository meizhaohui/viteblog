/* filename: struct_function.c */
#include <math.h>
#include <stdio.h>

// 定义结构体point，表示一个点
// x代表横坐标，y代表纵坐标
// 由struct引入结构声明
// point是结构的名称，也就是结构标记
struct point {
    int x;    // x是结构的成员，代表横坐标
    int y;    // y也是结构的成员，代表纵坐标
};

/* 获取矩形的面积 */
struct rectangle {
    // 本结构用于演示结构的嵌套
    struct point pt1;    // pt1是结构的成员，代表矩形左下角点的坐标
    struct point pt2;    // pt2也是结构的成员，代表矩形右上角点坐标
};

/* 通过x,y坐标构造一个点 */
struct point makepoint(int x, int y);
/* 将两个点相加 */
struct point addpoint(struct point p1, struct point p2);
/* 判断点p是否在矩形r中，在则返回1，否则返回0 */
int pointinrect(struct point p, struct rectangle r);

int main( )
{
    // 定义结构实例pt,即定义一个struct point类型的变量pt
    struct point pt;

    // 使用makepoint动态生成一个点
    int x = 1;
    int y = 2;
    pt    = makepoint(x, y);
    printf("点pt的坐标为: (%d, %d)\n", pt.x, pt.y);
    // 再构建一个点
    struct point new_pt;
    new_pt = makepoint(1, 1);
    printf("点new_pt的坐标为: (%d, %d)\n", new_pt.x, new_pt.y);

    // 对点执行算术运算
    struct point add_pt;
    add_pt = addpoint(pt, new_pt);
    // 因为结构类型参数是通过值传递的，所有makepoint函数执行后，并不会改变原来pt的坐标属性
    // 再次打印pt的坐标仍然是(1, 2)
    printf("点pt的坐标为: (%d, %d)\n", pt.x, pt.y);
    printf("点add_pt的坐标为: (%d, %d)\n", add_pt.x, add_pt.y);

    // 初始化矩形两个点
    // 坐标pt1为左下角点，pt2为右上角点
    struct rectangle rec = {{1, 2}, {3, 4}};
    printf("矩形左下角点的坐标为: (%d, %d)\n", rec.pt1.x, rec.pt1.y);
    printf("矩形右上角点的坐标为: (%d, %d)\n", rec.pt2.x, rec.pt2.y);

    printf("点pt在矩形rec内吗？%d\n", pointinrect(pt, rec));
    printf("点new_pt在矩形rec内吗？%d\n", pointinrect(new_pt, rec));
    printf("点add_pt在矩形rec内吗？%d\n", pointinrect(add_pt, rec));

    return 0;
}

/* 通过x,y坐标构造一个点 */
struct point makepoint(int x, int y)
{
    struct point temp;

    temp.x = x;
    temp.y = y;

    return temp;
}

/* 将两个点相加 */
struct point addpoint(struct point p1, struct point p2)
{
    // 结构类型的参数和其他类型的参数一样，都是通过值传递的
    p1.x += p2.x;
    p1.y += p2.y;

    return p1;
}

/* 判断点p是否在矩形r中，在则返回1，否则返回0 */
int pointinrect(struct point p, struct rectangle r)
{
    return p.x >= r.pt1.x && p.x <= r.pt2.x && p.y > r.pt1.y && p.y <= r.pt2.y;
}
