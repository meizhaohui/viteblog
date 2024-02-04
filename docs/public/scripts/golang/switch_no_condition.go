/*
 *      Filename: switch_no_condition.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 没有条件的switch语句
 *   Create Time: 2019-12-07 20:58:19
 * Last Modified: 2019-12-07 21:05:15
 */
package main

import (
	"fmt"
	"time"
)

func main() {
	nowtime := time.Now()
	switch {
	case nowtime.Hour() < 12:
		fmt.Println("Good morning!")
	case nowtime.Hour() < 17:
		fmt.Println("Good afternoon!")
	default:
		fmt.Println("Good evening!")
	}
}
