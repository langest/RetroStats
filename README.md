Stats for retropie games

# Manual install
Append the contents of runcommand_hooks to their respective runcommand hook in retropie.
```
$ cat runcommand_hook/sruncommand-onstart.sh >> /opt/retropie/configs/all/runcommand-onstart.sh
$ cat runcommand_hook/sruncommand-onend.sh >> /opt/retropie/configs/all/runcommand-onend.sh
```

# Running the program
On RPi python 2 is the default python so you need to call it with `python3`
```
$ python3 retro-stats/game_stats.py -f ~/RetroPie/game_stats.log
```

For a full list of option use `-h` or `--help`
```
usage: game_stats.py [-h] [-n LIST_LENGTH] [-f FILE] [-c CRITERIA]
                     [-m MINIMUM_SESSION_LENGTH] [-s SYSTEMS [SYSTEMS ...]]
                     [-e EXCLUDE_SYSTEMS [EXCLUDE_SYSTEMS ...]]
                     [-d DAILY_SCHEDULE | -b BAR_CHART]

Calculate some play statistics for your retro gaming

optional arguments:
  -h, --help            show this help message and exit
  -n LIST_LENGTH, --list-length LIST_LENGTH
                        how many entries to print int the top list, defaults
                        to 25
  -f FILE, --file FILE  path to the stats file, defaults to
                        /home/pi/RetroPe/game_stats.log
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
  -d DAILY_SCHEDULE, --daily-schedule DAILY_SCHEDULE
                        display daily time schedule, integer sets bar length
  -b BAR_CHART, --bar-chart BAR_CHART
                        display bar chart instead of numbers, integer sets bar
                        length
```
