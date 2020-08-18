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
        api_data = self.api_post_create_device(data)
        self.config["bikecitizens"]["uuid"] = api_data["device"]["uuid"]
        return api_data

    def login(self, login, password):
        user_data = self.api_post_sessions(login, password)
        self.config["bikecitizens"]["api_key"] = user_data["user"]["secret_token"]
        self.config["bikecitizens"]["user_id"] = str(user_data["user"]["id"])
        self.config["bikecitizens"]["username"] = str(user_data["user"]["username"])
        return user_data

    def get_user_id(self):
        return self.config["bikecitizens"].get("user_id")

    def get_username(self):
        return self.config["bikecitizens"].get("username")

    def is_logged_in(self):
        return self.config["bikecitizens"].get("api_key") is not None

    def save_config(self, config_path):
        configuration.save_config(config_path, self.config)

    #############################
    ######## API Methods ########
    #############################

    def api_post_create_device(self, data):
        req = self.session.post(f"{self.API_BASE}/devices.json", data=data)
        if not req.ok:
            raise RequestException(f"Error creating device: {req.text}")
        return req.json()

    def api_get_campaigns(self):
        req = self.session.get(f"{self.API_BASE}/campaigns.json")
        if not req.ok:
            raise RequestException(f"Error getting campaigns: {req.text}")
        return req.json()

    def api_get_device_sync(self, device_id):
        req = self.session.get(f"{self.API_BASE}/devices/{device_id}/sync.json")
        if not req.ok:
            raise RequestException(f"Error getting device sync: {req.text}")
        return req.json()

    # TODO: push register

    def api_get_pings_categories(self):
        req = self.session.get(f"{self.API_BASE}/pings/categories.json")
        if not req.ok:
            raise RequestException(f"Error getting pings categories: {req.text}")
        return req.json()

    def api_post_sessions(self, login, password):
        req = self.session.post(
            f"{self.API_BASE}/sessions.json",
            data={"login": login, "password": password},
        )
        if not req.ok:
            raise RequestException(f"Error in POST to sessions.json: {req.text}")
        return req.json()

    def api_get_tracks_user(self, user_id):
        req = self.session.get(
            f"{self.API_BASE}/tracks/user/{user_id}", headers=self.__get_headers()
        )
        if not req.ok:
            raise RequestException(f"Error getting tracks: {req.text}")

        return req.json()

    def api_get_track_points(self, track_id):
        req = self.session.get(
            f"{self.API_BASE}/tracks/{track_id}/points", headers=self.__get_headers()
        )
        if not req.ok:
            raise RequestException(f"Error getting track: {req.text}")

        return req.json()
