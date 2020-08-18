# Pykecitizens - An Inofficial Bike Citizens Api Client [WIP]

This repository contains a small client for the [Bikecitizens](https://bikecitizens.net) API.

> :warning: This project is not affiliated with bikecitizens.

> :warning: This is a work in progress project. Everything might change. I'm very happy to review PRs.

## Usage

### Installation

First, install all dependencies:

```
python -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

### Login

To really use the API, you need to login.
Creating an account is not yet supported.
To login, run

```
python src/login.py LOGIN PASSWORD
```

This creates a `config.ini` file which contains the login secret used by other tools and the api client.

### Tools

#### Export all tracks

To export all tracks in your bikecitizens account as gpx files, run

```
$ python src/export_all.py OUTPUT_DIRECTORY
```

### API

If you want to write own stuff using the bikecitizens api, you can use the `BikeCitizensApiClient` in `src/api_client.py`.
The only parameter needed is the path of the config file.
If no file with that name exists, an empty config is used.

```
>>> import api_client
>>> client = api_client.BikeCitizensApiClient(CONFIG_FILE)
```

#### Login

To check if the user is currenty logged in, use the `is_logged_in` method:

```
>>> client.is_logged_in()
False
```

To login, call the `login` method of the api client.
The first parameter can either be the username of the email of an account.

```
>>> client.login(LOGIN, PASSWORD)
{"user": ...}
>>> client.is_logged_in()
True
```

This logins the api client temporarily.

> :warning: This does not persist the created credentials. See the `Saving the config` section for this.

#### Saving the config

After performing methods that alter the configuration, it is important to call the `save_config` method on the client.
The only parameter needed is the path of the config file.
If no file with that name exists, a new one is created.

```
>>> client.save_config(CONFIG_FILE)
```

#### Getting user information

When the user is logged in, the user data is returned by the api.
Some of that data, especially the userid and username are save in the config file.
You can use the `get_user_id` and `get_username`:

```
>>> client.is_logged_in()
True
>>> client.get_username()
pajowu
>>> client.get_user_id()
123456
```

#### Methods

The client contains to types of methods: some that directly talk to the api, and some that do some more.
Those who directly talk to the api have a name of the scheme `api_REQUEST-METHOD_NAME`, where `REQUEST-METHOD` is either `post` or `get`.
The other methods have

## Configuration

Persistent data (most importantly, the API key) is saved in a configuration file.
This is a ini file created using pythons `configparser` module.
The filename defaults to `config.ini`.
All data regarding the api is stored in the `bikecitizens` section.
