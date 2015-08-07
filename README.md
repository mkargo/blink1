A simple visual timing device using a blink(1) gadget, intended for use by
conference speakers or session chairs to keep track of time.
The blink(1) stays green during the majority of the talk, turns orange when 
the allocated time is 70% elapsed, and flashes red when time expires.

Requirements: blink1-tool is in your path and can be run without sudo
Usage: blink1.py -d|-e hh:mm:ss [-o hh:mm:ss]
  where  -d, --duration specifies the total duration of the talk
         -e, --end      specifies the end time of the talk
         -o, --orange   specifies time before blink(1) turns orange (optional)
Either duration OR end MUST be specified.
Quits if the given end time has already passed.

Author: mkargo 20150807

