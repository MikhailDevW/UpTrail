import json
import math

import xmltodict

from gpx_converter import Converter

import gpxpy
import gpxpy.gpx

from test_utils import get_distance

def converting_gpx_to_json():
    x = Converter(
        input_file="../backend/src_develop/4373022.gpx"
    ).gpx_to_json(
        output_file="test.json"
    )


def read_json():
    with open("test.json") as open_json_gpx:
        print("JSON", open_json_gpx.read())


def read_gpx():
    with open("../backend/src_develop/develop.gpx") as open_gpx:
        xxx = open_gpx.read()
        yyy = xmltodict.parse(xxx)
        return yyy


with open("../backend/src_develop/develop.gpx") as open_gpx:
    gpx = gpxpy.parse(open_gpx)

route_track = []
if gpx.version == "1.1":
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                route_track.append(
                    {
                        'latitude': point.latitude,
                        'longitude': point.longitude,
                        'elevation': point.elevation
                    }
                )
else:
    for wp in gpx.waypoints:
        route_track.append(
            {
                'latitude': wp.latitude,
                'longitude': wp.longitude,
                'elevation': wp.elevation
            }
        )


def test():
    start_lat = route_track[0]['latitude']
    finish_lat = route_track[-1]['latitude']
    start_long = route_track[0]['longitude']
    finish_long = route_track[-1]['longitude']

    distance = get_distance(start_lat, finish_lat, start_long, finish_long)
    print("Протяженность маршрута:", distance, "км")


test()