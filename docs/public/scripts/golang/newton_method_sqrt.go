/*
 *      Filename: newton_method_sqrt.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 使用牛顿法(Newton Method)求平方根  x -= (x*x - F)/(x*x)
 *   Create Time: 2019-12-07 19:31:30
 * Last Modified: 2019-12-07 20:20:15
 */
package main

import (
	"fmt"
	"math"
)

func newton(F float64) float64 {
	guess_num := 1
	x := float64(1)
	for math.Abs(x*x-F) > 1e-10 {
		fmt.Printf("第%d次猜值为%f\n", guess_num, x)
		x -= (x*x - F) / (2 * x)
		guess_num++
	}
	return x

}

func main() {
	fmt.Println("库函数求平方根math.Sqrt(8) =", math.Sqrt(8))
	fmt.Println("牛顿法求平方根newton(8) =", newton(8))
}
