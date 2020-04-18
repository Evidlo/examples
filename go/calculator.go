// Evan Widloski - 2019-04-04
// a calculator which prompts the user for input and writes the result to a file

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	str := strings.TrimSpace(reader.ReadString('\n'))
	fmt.Println(strconv.ParseFloat(str, 64))
}
