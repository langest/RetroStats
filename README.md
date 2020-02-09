Stats for RetroPie games, and any other games that write to the `game_stats.log`

Development discussion and preview is available on the official RetroPie forum,
in a thread about the development of this tool, [Link](https://retropie.org.uk/forum/topic/24756/retrostats-web-application).

# Preview
## Desktop

<details><summary>Desktop</summary>
   <img src="https://retropie.org.uk/forum/assets/uploads/files/1580642874924-1.png" alt="Desktop Histogram 1">
   <img src="https://retropie.org.uk/forum/assets/uploads/files/1580642874942-2.png" alt="Desktop Histogram 2">
   <img src="https://retropie.org.uk/forum/assets/uploads/files/1580642875009-3.png" alt="Desktop Schedule">
</details>

## Mobile
<details><summary>Desktop</summary>
   <img src="https://retropie.org.uk/forum/assets/uploads/files/1580642874806-4.png" alt="Mobile Histogram ">
   <img src="https://retropie.org.uk/forum/assets/uploads/files/1580642874807-5.png" alt="Mobile Schedule">
</details>

# Dependencies
pip for python 3
```
# apt install python3-pip
```

# Manual install
Instal using pip in repo root
```
$ pip3 install . --user
```

Append the contents of runcommand_hooks to their respective runcommand hook in RetroPie.
```
$ cat runcommand_hooks/runcommand-onstart.sh >> /opt/retropie/configs/all/runcommand-onstart.sh
$ cat runcommand_hooks/runcommand-onend.sh >> /opt/retropie/configs/all/runcommand-onend.sh
```

If you want the web server to automatically start
Edit crontab using `# crontab -e`
Add the following
```
@reboot retro-stats-server &
```

Reboot your Raspberry Pi
Now the web server will start automatically and you can open a browser and go to <your-rpi-ip>:8080 to show your statistics.
See the instructions below on how to use a different port.

# Running the program

## Running using Command Line Tool
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

## Running Web Server
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
After starting the server, open a browser and go to your Raspberry Pi's ip followed by the portnumber.
`<pi-ip>:<port number>, default port number is 8080.
If you run with a custom port number make sure to add that to the URL.

# Roadmap
There is no time frame for when the features will be implemented,
this is something I do in my spare time so the time I can invest is limited.
Upcoming features in no particular order:
* Automate installation
* Cache data in web client for faster and more responsive graph updates
* Add historical data functionality from cli to the web gui as well
