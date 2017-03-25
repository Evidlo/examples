#!/usr/bin/env lua
-- Evan Widloski - 2017-03-25
-- mpv status script for CD5220 based LCDs
-- alternates between displaying track title and playback time

local display_progress_counter = 5
local f = assert(io.open("/dev/ttyUSB0", "a"))

-- scrolls track title on top bar
function display_title()
  local title = mp.get_property("media-title", " ")

  f:write("\12")
  f:write("\27\81\68")
  f:write(title)
  f:write("\13")

  f:flush()

  mp.add_timeout(10, display_progress)
end


-- displays current playback time and a graphical bar
function display_progress()
  local percent = mp.get_property("percent-pos", 0)
  local time = mp.get_property_osd("playback-time", "00:00:00")
  local duration = mp.get_property_osd("duration", "00:00:00")

  local num_hashes = (percent * 18)/100
  local bar = string.format("[%s%s]", string.rep("#", num_hashes), string.rep(" ", 18 - num_hashes))
  local playtime = string.format("%s / %s", time, duration)

  -- display time
  f:write("\12")
  f:write("\27\81\65")
  f:write(playtime)
  f:write("\13")

  -- display progress bar
  f:write("\27\81\66")
  f:write(bar)
  f:write("\13")

  f:flush()

  if display_progress_counter > 0 then
    mp.add_timeout(1, display_progress)
    display_progress_counter = display_progress_counter - 1
  else
    display_progress_counter = 5
    display_title()
  end
end


-- clear display when mpv exits
local function clear()
  f:write("\12")

  f:close()
end


mp.register_event("file-loaded", display_title)
mp.register_event("shutdown", clear)
