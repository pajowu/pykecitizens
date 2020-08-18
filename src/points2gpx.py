import datetime

import gpxpy
import gpxpy.gpx


def points2gpx(out_file, points, point_time):
    gpx = gpxpy.gpx.GPX()

    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)

    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)

    for point in points:
        point_time += datetime.timedelta(milliseconds=point["delta"])
        segment.points.append(
            gpxpy.gpx.GPXTrackPoint(
                point["lat"], point["lon"], elevation=point["ele"], time=point_time
            )
        )

    out_file.write(gpx.to_xml())
