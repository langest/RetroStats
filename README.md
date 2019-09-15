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
usage: game_stats.py [-h] [-n LIST_LENGTH] [-f FILE] [-c CRITERIA] [-s SYSTEM]
                     [-m MINIMUM_SESSION_LENGTH]

Calculate some play statistics for your retro gaming

optional arguments:
  -h, --help            show this help message and exit
  -n LIST_LENGTH, --list-length LIST_LENGTH
                        how many entries to print int the top list
  -f FILE, --file FILE  path to the stats file
  -c CRITERIA, --criteria CRITERIA
                        which criteria to order by, available options are:
                        total (time), times (played), average (session
                        length), median (session length), defaults to total
  -s SYSTEM, --system SYSTEM
                        the system you want statistics for, if omitted, will
                        use all systems
  -m MINIMUM_SESSION_LENGTH, --minimum-session-length MINIMUM_SESSION_LENGTH
                        skip sessions shorter than this number of seconds,
                        defaults to 120
```
