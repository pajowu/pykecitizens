import uuid

import requests

import configuration


class RequestException(Exception):
    pass


class BikeCitizensApiClient:
    API_BASE = "https://api.bikecitizens.net/api/v1"

    def __init__(self, config_path):
        self.config = configuration.load_config(config_path)
        if not self.config.has_section("bikecitizens"):
            self.config.add_section("bikecitizens")
        self.session = requests.Session()

    def __get_headers(self):
        return {"X-API-Key": self.config["bikecitizens"]["api_key"]}

    def create_device(self):
        data = {
            "uuid": str(uuid.uuid4()),
            "device[phone_brand]": "n/a",
            "device[phone_model]": "n/a",
            "device[phone_os]": "n/a",
            "device[app_version]": "n/a",
            "device[app_code]": "n/a",
        }
        req = self.session.post(f"{self.API_BASE}/devices.json", data=data)
        if req.ok:
            self.config["bikecitizens"]["uuid"] = req.json()["device"]["uuid"]
        else:
            raise RequestException(f"Creating device: {req.text}")
        return req.json()

    # TODO: /campaigns.json
    # TODO: devices/DEVICE_ID/sync.json
    # TODO: push register

    def login(self, login, password):
        req = self.session.post(
            f"{self.API_BASE}/sessions.json",
            data={"login": login, "password": password},
        )
        if req.ok:
            self.config["bikecitizens"]["api_key"] = req.json()["user"]["secret_token"]
            self.config["bikecitizens"]["user_id"] = str(req.json()["user"]["id"])
            self.config["bikecitizens"]["username"] = str(
                req.json()["user"]["username"]
            )
        else:
            raise RequestException(f"Error logging in: {req.text}")

        return req.json()

    def get_user_id(self):
        return self.config["bikecitizens"].get("user_id")

    def get_username(self):
        return self.config["bikecitizens"].get("username")

    def is_logged_in(self):
        return self.config["bikecitizens"].get("api_key") is not None

    def get_tracks(self, user_id):
        req = self.session.get(
            f"{self.API_BASE}/tracks/user/{user_id}", headers=self.__get_headers()
        )
        if not req.ok:
            raise RequestException(f"Error getting tracks: {req.text}")

        return req.json()

    def get_track(self, track_id):
        req = self.session.get(
            f"{self.API_BASE}/tracks/{track_id}/points", headers=self.__get_headers()
        )
        if not req.ok:
            raise RequestException(f"Error getting track: {req.text}")

        return req.json()

    def save_config(self, config_path):
        configuration.save_config(config_path, self.config)
