package main

import (
	"fmt"
	"github.com/gdamore/tcell"
	"github.com/renstrom/fuzzysearch/fuzzy"
	"github.com/rivo/tview"
	"log"
	"os"
	"sort"
	"strconv"
	"time"
)

func say(s string) {
	for true {
		time.Sleep(100 * time.Millisecond)
		fmt.Println(s)
	}
}

type GomuksUI struct {
	views    *tview.Pages
	app      *tview.Application
	rooms    *[]string
	MainView *tview.TextView
	logger   *log.Logger
}

type FuzzySearch struct {
	*tview.Grid
	matches fuzzy.Ranks
}

func NewFuzzySearch(ui GomuksUI, width int, height int) *FuzzySearch {

	// search box for fuzzy search
	fuzzy_search := tview.NewInputField().
		SetLabel("Room: ")

	// list of rooms matching fuzzy search
	fuzzy_results := tview.NewTextView().
		SetDynamicColors(true).
		SetRegions(true).
		SetChangedFunc(
			func() {
				ui.app.Draw()
			})

	// flexbox containing input box and results
	fuzzy_flex := tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(fuzzy_search, 0, 1, true).
		AddItem(fuzzy_results, 0, 1, false)

	fuzzy_flex.SetBorder(true).
		SetTitle("Fuzzy Room Finder")

	var matches fuzzy.Ranks
	fuzz := &FuzzySearch{
		Grid: tview.NewGrid().
			SetColumns(0, width, 0).
			SetRows(0, height, 0).
			AddItem(fuzzy_flex, 1, 1, 1, 1, 0, 0, true),
		matches: matches,
	}

	// callback to update search box
	input_callback := func(str string) {
		ui.logger.Println("rooms: ", *ui.rooms)
		ui.logger.Println("matches: ", fuzz.matches)
		fuzz.matches = fuzzy.RankFind(str, *ui.rooms)
		if len(str) > 0 && len(fuzz.matches) > 0 {
			sort.Sort(fuzz.matches)
			fuzzy_results.Clear()
			for region_id, match := range fuzz.matches {
				fmt.Fprintf(fuzzy_results, "[\"%d\"]%s[\"\"]\n", region_id, match.Target)
			}
			fuzzy_results.Highlight("0")
			fuzzy_results.ScrollToBeginning()
		} else {
			fuzzy_results.Clear()
			fuzzy_results.Highlight()
		}

	}

	// callback to handle key events on fuzzy search
	input_key_callback := func(event *tcell.EventKey) *tcell.EventKey {
		highlights := fuzzy_results.GetHighlights()
		if event.Key() == tcell.KeyEsc {
			ui.views.RemovePage("modal")
			return nil
		} else if event.Key() == tcell.KeyTab {
			new_selection := 0
			if len(highlights) > 0 {
				selected_region, err := strconv.Atoi(highlights[0])
				if err != nil {
					panic(err)
				}
				new_selection = (selected_region + 1) % len(fuzz.matches)
			}
			fuzzy_results.Highlight(strconv.Itoa(new_selection))
			fuzzy_results.ScrollToHighlight()
			return nil
		} else if event.Key() == tcell.KeyEnter {
			if len(highlights) > 0 {
				ui.MainView.SetText(fuzzy_results.GetRegionText(highlights[0]))
			} else if len(fuzz.matches) > 0 {
				ui.MainView.SetText(fuzz.matches[0].Target)
			}
			ui.views.RemovePage("modal")
			fuzzy_results.Clear()
			fuzzy_search.SetText("")
			return nil
		} else {
			return event
		}
	}

	fuzzy_search.SetChangedFunc(input_callback)
	fuzzy_search.SetInputCapture(input_key_callback)

	return fuzz
}

func main() {
	file, _ := os.Create("/tmp/log")
	logger := log.New(file, "log: ", log.Lshortfile)
	logger.Println("lkj")
	app := tview.NewApplication()

	rooms := []string{"room1", "room2", "room3", "z", "za", "zb", "zc", "zd", "ze", "zf", "Evan Widloski", "cat", "cat attack"}

	// placeholder to show currently selected room
	MainView := tview.NewTextView().
		SetTextColor(tcell.ColorBlue)

	views := tview.NewPages().
		AddPage("MainView", MainView, true, true)

	ui := GomuksUI{
		views:    views,
		app:      app,
		rooms:    &rooms,
		MainView: MainView,
		logger:   logger,
	}

	logger.Println("rooms: ", rooms)

	// callback to handle key events on bg view
	mainview_key_callback := func(event *tcell.EventKey) *tcell.EventKey {
		if event.Key() == tcell.KeyCtrlSpace {
			views.AddPage("modal", NewFuzzySearch(ui, 40, 10), true, true)
			return nil
		} else {
			return event
		}
	}

	ui.MainView.SetInputCapture(mainview_key_callback)

	go say("foobar")
	// say("lkj")

	err := app.SetRoot(views, true).Run()
	if err != nil {
		panic(err)
	}

}
