/*
 *      Filename: named_results.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 命名返回值
 *   Create Time: 2019-11-24 23:22:51
 * Last Modified: 2019-11-24 23:29:32
 */
package main

import "fmt"

func split(sum int) (x, y int) {
	x = sum * 2 / 3
	y = sum - x
	return
}
func main() {
	fmt.Println(split(14))
}
