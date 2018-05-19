package main

import (
	"fmt"
	"github.com/gdamore/tcell"
	"github.com/renstrom/fuzzysearch/fuzzy"
	"github.com/rivo/tview"
	"sort"
	"strconv"
	"strings"
)

func main() {
	app := tview.NewApplication()

	// a function which returns a modal containing some widget
	modal := func(p tview.Primitive, width, height int) tview.Primitive {
		return tview.NewGrid().
			SetColumns(0, width, 0).
			SetRows(0, height, 0).
			AddItem(p, 1, 1, 1, 1, 0, 0, true)
	}

	rooms := []string{"room1", "room2", "room3", "Evan Widloski", "cat", "cat attack"}
	var matches fuzzy.Ranks

	// placeholder to show currently selected room
	background := tview.NewTextView().
		SetTextColor(tcell.ColorBlue)

	input_field := tview.NewInputField().
		SetLabel("Room: ")

	fuzzy_results := tview.NewTextView().
		SetDynamicColors(true).
		SetRegions(true).
		SetChangedFunc(
			func() {
				app.Draw()
			})

	// flexbox containing input box and results
	fuzzy_flex := tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(input_field, 0, 1, true).
		AddItem(fuzzy_results, 0, 1, false)

	pages := tview.NewPages().
		AddPage("background", background, true, true)

	// callback to update background with selected room
	input_callback := func(str string) {
		matches = fuzzy.RankFind(str, rooms)
		if len(str) > 0 && len(matches) > 0 {
			sort.Sort(matches)
			fuzzy_results.Clear()
			for region_id, match := range matches {
				fmt.Fprintf(fuzzy_results, "[\"%d\"]%s[\"\"]\n", region_id, match.Target)
			}
		} else {
			fuzzy_results.Clear()
			fuzzy_results.Highlight()
		}

	}

	// callback to handle key events on fuzzy search
	input_key_callback := func(event *tcell.EventKey) *tcell.EventKey {
		highlights := fuzzy_results.GetHighlights()
		if event.Key() == tcell.KeyEsc {
			pages.RemovePage("modal")
			return nil
		} else if event.Key() == tcell.KeyTab {
			new_selection := 0
			if len(highlights) > 0 {
				selected_region, err := strconv.Atoi(highlights[0])
				if err != nil {
					panic(err)
				}
				new_selection = (selected_region + 1) % len(matches)
			}
			fuzzy_results.Highlight(strconv.Itoa(new_selection))
			return nil
		} else if event.Key() == tcell.KeyEnter {
			if len(highlights) > 0 {
				background.SetText(fuzzy_results.GetRegionText(highlights[0]))
			}
			pages.RemovePage("modal")
			fuzzy_results.Clear()
			input_field.SetText("")
			return nil
		} else {
			return event
		}
	}

	// callback to handle key events on bg view
	background_key_callback := func(event *tcell.EventKey) *tcell.EventKey {
		if event.Key() == tcell.KeyCtrlSpace {
			pages.AddPage("modal", modal(fuzzy_flex, 40, 10), true, true)
			return nil
		} else {
			return event
		}
	}

	background.SetInputCapture(background_key_callback)
	input_field.SetChangedFunc(input_callback)
	input_field.SetInputCapture(input_key_callback)

	err := app.SetRoot(pages, true).Run()
	if err != nil {
		panic(err)
	}

}
