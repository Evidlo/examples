package main

import (
	"fmt"
	"flag"
	"log"
	"io/ioutil"
	"net/http"
	"github.com/antchfx/htmlquery"
)

func main() {
	url := flag.String("url", "", "input URL")
	xpath := flag.String("xpath", "", "xpath expression")
	flag.Parse()

	if *url == "" {
		log.Fatal("url is required")
	}
	if *xpath == "" {
		log.Fatal("xpath is required")
	}

	response, err := http.Get(*url)
	if err != nil {
		panic(err)
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		body, _ := ioutil.ReadAll(response.Body)
		log.Fatal(body)
	}

	doc, err := htmlquery.Parse(response.Body)
	if err != nil {
		panic(err)
	}

	e := htmlquery.FindOne(doc, *xpath)

	fmt.Println(e)
	// fmt.Println(e.Val)
}
