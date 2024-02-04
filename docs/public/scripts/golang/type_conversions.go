/*
 *      Filename: type_conversions.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 数据类型转换
 *   Create Time: 2019-12-07 15:01:38
 * Last Modified: 2019-12-07 15:18:27
 */
package main

import (
	"fmt"
	"math"
)

func main() {
	var i int = 42
	var f float64 = float64(i)
	var u uint = uint(f)
	fmt.Println(i, f, u)

	x, y := 3, 4
	z := math.Sqrt(float64(x*x + y*y))
	fmt.Println(x, y, z)
}
