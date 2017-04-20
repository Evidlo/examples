// Evan Widloski
// 2017-02-02

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func hello() {
	fmt.Printf("hello universe!\n")
}

func vector() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Printf("input x1:\n")
	x1_str, err := reader.ReadString('\n')
	x1, err := strconv.ParseFloat(x1_str, 64)
	fmt.Println(x1 + 1)
	// fmt.Printf("input y1:\n")
	// y1, _ := reader.ReadString('\n')
	// y1 = strconv.Atoi(x1)
	// fmt.Printf("input z1:\n")
	// z1, _ := reader.ReadString('\n')
	// z1 = strconv.Atoi(x1)
	// fmt.Printf("input x2:\n")
	// x2, _ := reader.ReadString('\n')
	// x2 = strconv.Atoi(x1)
	// fmt.Printf("input y2:\n")
	// y2, _ := reader.ReadString('\n')
	// y2 = strconv.Atoi(x1)
	// fmt.Printf("input z2:\n")
	// z2, _ := reader.ReadString('\n')
	// z2 = strconv.Atoi(x1)

	// return x1*x2 + y1*y2 + z1*z2
	// return x1
}

func main() {
	hello()
	vector()
}
