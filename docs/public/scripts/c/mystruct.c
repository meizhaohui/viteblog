/* filename: mystruct.c */
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

/* 获取点到原点(0, 0)的距离 */
double get_distance(struct point pt);

/* 获取矩形的面积 */
int get_area(struct rectangle rec);

int main( )
{
    // 定义结构实例pt,即定义一个struct point类型的变量pt
    struct point pt;
    // 可以通过 结构名.成员 的形式来引用某个特定结构的成员
    // 结构名.成员 中间的点号.称为 成员运算符
    pt.x = 1;
    pt.y = 2;

    // automatic structure 自动结构可以使用赋值初始化
    // 自动结构 就是auto 修饰的结构变量.而auto是缺省的
    // 所以 只要不是static的局部结构体变量,都是自动结构
    struct point maxpt = {320, 200};

    printf("点pt的坐标为: (%d, %d)\n", pt.x, pt.y);
    printf("点pt到原点距离为: %.2f\n", get_distance(pt));
    printf("点maxpt的坐标为: (%d, %d)\n", maxpt.x, maxpt.y);
    printf("点maxpt到原点距离为: %.2f\n", get_distance(maxpt));

    // 初始化矩形两个点
    // 坐标pt1为左下角点，pt2为右上角点
    struct rectangle rec = {{1, 2}, {3, 4}};
    printf("矩形左下角点的坐标为: (%d, %d)\n", rec.pt1.x, rec.pt1.y);
    printf("矩形右上角点的坐标为: (%d, %d)\n", rec.pt2.x, rec.pt2.y);
    printf("矩形面积为: %d\n", get_area(rec));

    return 0;
}

/* 获取点到原点(0, 0)的距离 */
double get_distance(struct point pt)
{
    double dist;
    dist = sqrt((double) pt.x * pt.x + (double) pt.y * pt.y);

    return dist;
}

/* 获取矩形的面积 */
int get_area(struct rectangle rec)
{
    int area;
    area = (rec.pt2.x - rec.pt1.x) * (rec.pt2.y - rec.pt1.y);

    return area;
}