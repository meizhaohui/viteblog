/*
 *      Filename: base_if.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: if判断语句的使用
 *   Create Time: 2019-12-07 17:28:07
 * Last Modified: 2019-12-07 17:51:22
 */
package main

import (
	"fmt"
	"math"
	"os"
)

func sqrt(x float64) float64 {
	if x < 0 {
		fmt.Println("求平方根的数必须不小于0")
		os.Exit(1) // 退出程序
	}
	return math.Sqrt(x)
}

func main() {
	fmt.Println(sqrt(2))
	fmt.Println(sqrt(-2))
}
