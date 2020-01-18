Stats for retropie games

# Manual install
Append the contents of runcommand_hooks to their respective runcommand hook in retropie.
```
$ cat runcommand_hook/runcommand-onstart.sh >> /opt/retropie/configs/all/runcommand-onstart.sh
$ cat runcommand_hook/runcommand-onend.sh >> /opt/retropie/configs/all/runcommand-onend.sh
```

Instal using pip in repo root
```
$ pip install -e . --user
```

# Running the program

## Running using cli
```
$ retro-stats-cli -h
usage: retro-stats-cli [-h] [-n LIST_LENGTH] [-f FILE] [-c CRITERIA]
                       [-m MINIMUM_SESSION_LENGTH] [-s SYSTEMS [SYSTEMS ...]]
                       [-e EXCLUDE_SYSTEMS [EXCLUDE_SYSTEMS ...]]
                       [-l LOOKBACK] [-w | -b BAR_CHART | -r]

Calculate some play statistics for your retro gaming

optional arguments:
  -h, --help            show this help message and exit
  -n LIST_LENGTH, --list-length LIST_LENGTH
                        how many entries to print, defaults to 25
  -f FILE, --file FILE  path to the stats file, defaults to
                        /home/pi/RetroPie/game_stats.log
  -c CRITERIA, --criteria CRITERIA
                        which criteria to order by, disabled for schedule
                        option, available options are: total (time), times
                        (played), average (session length), median (session
                        length), defaults to total
  -m MINIMUM_SESSION_LENGTH, --minimum-session-length MINIMUM_SESSION_LENGTH
                        skip sessions shorter than this number of seconds,
                        defaults to 120
  -s SYSTEMS [SYSTEMS ...], --systems SYSTEMS [SYSTEMS ...]
                        the systems you want statistics for, default will use
                        all systems
  -e EXCLUDE_SYSTEMS [EXCLUDE_SYSTEMS ...], --exclude-systems EXCLUDE_SYSTEMS [EXCLUDE_SYSTEMS ...]
                        skip the listed systems, default no systems
  -l LOOKBACK, --lookback LOOKBACK
                        Number of days lookback to use for the stats, defaults
                        to no limit (0)
  -w, --weekly-schedule
                        display weekly time schedule
  -b BAR_CHART, --bar-chart BAR_CHART
                        display bar chart instead of numbers, integer sets bar
                        length
  -r, --recently_played
                        print your game history
```

## running webserver
```
$ retro-stats-server -h
usage: retro-stats-server [-h] [-p PORT] [-r REFRESH_INTERVAL] [-f FILE]

Calculate some play statistics for your retro gaming

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  portnumber for the server, defaults to 80
  -r REFRESH_INTERVAL, --refresh-interval REFRESH_INTERVAL
                        the number of minutes you want to cache the log
  -f FILE, --file FILE  path to the stats file, defaults to
                        /home/pi/RetroPie/game_stats.log
```
After starting the server, open a browser and go to your Raspberry Pi's ip.
If you run with a custom portnumber make sure to add that to the url.
