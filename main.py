#!/usr/bin/python3

import time, datetime

import pathlib

ImageIndex = int
Altitude = float
Azimuth = float
Position = tuple [Altitude, Azimuth]
Distance = float
def distance_between (pos1: Position, pos2: Position) -> Distance:
    import math
    return math.sqrt (((pos2 [0] - pos1 [0]) ** 2) + ((pos2 [1] - pos1 [1]) ** 2))

FilePath = pathlib.Path
def file_path_for (image_index: ImageIndex) -> FilePath:
    return pathlib.Path (__file__).parent / "mojave_dynamic" / f"mojave_dynamic_{image_index + 1}.jpeg"

def get_positions () -> dict [FilePath: Position]:
    import plistlib

    with open (pathlib.Path (__file__).parent / "Solar.plist", "rb") as data_file:
        solar_data = plistlib.load (data_file)

    return {file_path_for (image_info ["i"]): (image_info ["a"], image_info ["z"]) for image_info in solar_data ["si"]}
positions = get_positions ()

Latitude = float
Longitude = float
def get_current_location () -> (float, float):
    import geocoder
    loc = geocoder.ip ("me")
    return loc.latlng
current_location = get_current_location ()

def get_current_position () -> Position:
    import astropy.coordinates as coord
    from astropy.time import Time
    import astropy.units as u

    lat, lng = current_location

    loc = coord.EarthLocation (lon = lng * u.deg,
                               lat = lat * u.deg)
    now = Time (datetime.datetime.utcnow (), scale = "utc")

    altaz = coord.AltAz (location = loc, obstime = now)
    sun = coord.get_sun (now)

    to = sun.transform_to (altaz)
    return to.alt.deg, to.az.deg

def get_closest_file_path (_current_position: Position) -> FilePath:
    paths_and_positions = positions.items ()
    distances: dict [FilePath, Distance] = {}
    for path, position in paths_and_positions:
        distances [path] = distance_between (position, _current_position)
    sorted_distances = sorted (distances.items (), key = lambda pair: pair [1])
    return sorted_distances [0] [0]

class UnsupportedPlatformException (Exception): pass
def set_background (path: pathlib.Path):
    # noinspection PyUnresolvedReferences

    resolved_path = path.resolve ()

    import platform
    system = platform.system ()
    if system == "Linux":
        from gi.repository import Gio
        settings = Gio.Settings.new ("org.gnome.desktop.background")
        settings.set_string ("picture-uri", f"file://{resolved_path}")
        settings.apply ()
    elif system == "Windows":
        import ctypes
        SPI_SETDESKTOPWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW (SPI_SETDESKTOPWALLPAPER, 0, str (resolved_path), 0)
    else: raise UnsupportedPlatformException (f"No implementation for setting the wallpaper on {system}")

def auto_set_background ():
    current_position = get_current_position ()
    closest_file_path = get_closest_file_path (current_position)
    set_background (closest_file_path)

def do_auto_set_loop ():
    home_folder = pathlib.Path.home ()
    config_folder = home_folder / ".wallpaperyboi"
    if not config_folder.exists (): config_folder.mkdir ()
    config_file_name = "delay_seconds.txt"
    config_file_path = config_folder / config_file_name
    if not config_file_path.exists ():
        delay_seconds = 600 # 10 minutes
        with open (config_file_path, "w+") as config_file:
            config_file.write (str (delay_seconds))
    else:
        with open (config_file_path, "r") as config_file:
            delay_seconds = int (config_file.readline ())

    while True:
        start = time.perf_counter ()

        auto_set_background ()

        end = time.perf_counter ()
        time.sleep (delay_seconds - (end - start))

if __name__ == "__main__":
    do_auto_set_loop ()