/*
 *      Filename: constants.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 常量的使用
 *   Create Time: 2019-11-28 23:14:04
 * Last Modified: 2019-11-28 23:23:22
 */
package main

import "fmt"

const (
	Pi      = 3.14
	Version = "go1.13.3 linux/amd64"
)

func area(radius float32) float32 {
	return Pi * radius * radius
}

func main() {
	fmt.Println("Golang的版本号:", Version)
	fmt.Println("圆的面积:", area(2))
}
