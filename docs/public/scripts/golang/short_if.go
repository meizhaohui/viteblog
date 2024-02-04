/*
 *      Filename: short_if.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: if的便捷语句
 *   Create Time: 2019-12-07 17:55:50
 * Last Modified: 2019-12-07 18:07:43
 */
package main

import "fmt"

func main() {
	if num := 2; num > 0 {
		fmt.Println(num, "是正数")

	} else if num == 0 {
		fmt.Println(num, "为0")
	} else {
		fmt.Println(num, "是负数")
	}
}
