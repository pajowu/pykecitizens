import argparse

import api_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("login", help="Username or email")
    parser.add_argument("password")
    parser.add_argument("--config-file", default="config.ini")

    args = parser.parse_args()

    client = api_client.BikeCitizensApiClient(args.config_file)

    if client.is_logged_in():
        print(f"WARNING: Already logged in as {client.get_username()}")
        print("Press any key to continue")
        input()

    print(f"Logging in as {args.login}")
    client.login(args.login, args.password)
    print(f"Successfully logged in as {client.get_username()}")
    client.save_config(args.config_file)
    print(f"Credentials save to {args.config_file}")
