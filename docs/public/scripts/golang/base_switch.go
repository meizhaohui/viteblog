/*
 *      Filename: base_switch.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: switch语句的使用
 *   Create Time: 2019-12-07 20:45:40
 * Last Modified: 2019-12-07 20:50:00
 */
package main

import "fmt"
import "runtime"

func main() {
	fmt.Print("Golang runs on ")
	switch os := runtime.GOOS; os {
	case "windows":
		fmt.Println("Windows System")
	case "linux":
		fmt.Println("Linux System")
	default:
		fmt.Printf("%s System", os)

	}
}
