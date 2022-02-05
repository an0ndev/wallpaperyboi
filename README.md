# Wallpapery Boi

Mojave dynamic wallpaper for Windows/Linux. (beware, 3am jank present)

## Setup
- Windows
  - install recent Python, tested on 3.10.2
  - dependencies: `pip install geocoder astropy`
  - add shortcut to `<Python folder>\pythonw.exe <repo folder>\main.py` in `%AppData%\Microsoft\Windows\Start Menu\Programs\Startup`
  - profit
- Linux (GNOME)
  - dependencies: `pip install geocoder astropy PyGObject`
  - `chmod +x main.py` (shebang is already present)
  - add as startup application
  - profit

## Update frequency
The number of seconds between update is stored in `<home folder>/.wallpaperyboi/delay_seconds.txt`. (restart app after modifying)

## References
- https://gist.github.com/ole/6b6b5ef20fbec12e9227075e20c6e6ef
- http://files.rb.gd/mojave_dynamic.zip
- https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python
- https://stackoverflow.com/questions/47663082/how-can-we-compute-solar-position-at-a-given-place-on-a-given-day-and-time
- https://askubuntu.com/questions/791434/changes-via-gio-settings-dont-take-effect
- https://askubuntu.com/questions/37957/how-do-i-manage-applications-on-startup-in-gnome-3