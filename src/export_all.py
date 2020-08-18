import argparse
import datetime
import os
import sys

import api_client
from points2gpx import points2gpx

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", default="config.ini")
    parser.add_argument("--user_id", default=None)
    parser.add_argument("out_dir")
    args = parser.parse_args()

    client = api_client.BikeCitizensApiClient(args.config_file)

    if not client.is_logged_in():
        print("ERROR: Need to be logged in")
        sys.exit(-1)

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    user_id = args.user_id
    if user_id is None:
        user_id = client.get_user_id()

    user_tracks = client.get_tracks(user_id)

    for track in user_tracks:
        track_start_time = datetime.datetime.strptime(
            track["start_time"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        print(f"Dumping Track {track['id']}")
        points = client.get_track(track["id"])
        with open(os.path.join(args.out_dir, f"{track['id']}.gpx"), "w") as f:
            points2gpx(f, points, track_start_time)
