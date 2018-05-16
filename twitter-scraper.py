#!/usr/bin/python3
import sqlite3
import twitter
import argparse
import re, os, sys
import requests
from watson_developer_cloud import PersonalityInsightsV2

# Twitter API
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""

# IBM Watson API (PersonalityInsights)
USERNAME = ""
PASSWORD = ""

def scrape_all(api, conn, c, args):

    name_dictionary = args.dictionary

    def analyse(username):
        statuses = api.GetUserTimeline(screen_name=username, count=200, include_rts=False)
        text = ""
        for s in statuses:
            if (s.lang == 'en'):
                text += s.text

        user_personality = PersonalityInsightsV2(username=USERNAME, password=PASSWORD).profile(text)

        return user_personality

    def check_geolocations(username):
        try:
            locations = []
            statuses = api.GetUserTimeline(screen_name=username)
            for s in statuses:
                if s.place:
                    coordinates = s.place['bounding_box']['coordinates']
                    locations.append(coordinates)

            return locations
        except twitter.error.TwitterError:
            return None

    def check_for_credentials(users):
        def check():
            c.execute("SELECT COUNT(*) FROM users WHERE username=?", (user.screen_name,))
            occurences = c.fetchone()[0]
            if not occurences:
                emails = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+$', user.description)
                phones = re.findall(r'(?:(?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(?:0\d|\(?:[0-9]{3}\)|[1-9]{0,3})(?:(?:(?: |\-)[0-9]{2}){4}|(?:(?:[0-9]{2}){4})|(?:(?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|(?:[0-9]{7}))', user.description)

                if emails or phones:
                    c.execute("INSERT INTO users ('username') VALUES (?)", (user.screen_name,))
                    conn.commit()
                if emails:
                    email_entry = ""
                    for index, email in enumerate(emails):
                        print("[\033[92mFOUND\033[0m] Email for @{}: {}".format(user.screen_name, email))
                        if (len(emails) > 1) and (index > 0):
                            email_entry += ",{}".format(email)
                        else:
                            email_entry = email
                    c.execute("UPDATE users SET email=? WHERE username=?", (email_entry, user.screen_name))
                    conn.commit()
                if phones:
                    phone_entry = ""
                    for index, phone in enumerate(phones):
                        print("[\033[92mFOUND\033[0m] Phone for @{}: {}".format(user.screen_name, phone))
                        if (len(phones) > 1) and (index > 0):
                            phone_entry += ",{}".format(phone)
                        else:
                            phone_entry = phone
                    c.execute("UPDATE users SET phone=? WHERE username=?", (phone_entry, user.screen_name))
                    conn.commit()
                if emails or phones:
                    if args.analyse:
                        print("[*] Building profile for @{}... ".format(user.screen_name), end="")
                        sys.stdout.flush()
                        profile = analyse(user.screen_name)
                        print("\033[92mDONE\033[0m")
                        c.execute("UPDATE users SET personality=? WHERE username=?", (str(profile), user.screen_name))
                        conn.commit()
                    if args.geolocations:
                        locations = check_geolocations(user.screen_name)
                        if locations:
                            print("[\033[92mFOUND\033[0m] Geolocations for @{}".format(user.screen_name))
                            c.execute("UPDATE users SET locations=? WHERE username=?", (str(locations), user.screen_name))
                            conn.commit()

        for user in users:
            if args.verified:
                if user.verified:
                    check()
            else:
                check()


    with open(name_dictionary, 'r') as names:
        for name in names:
            if not args.quiet:
                print("[*] Searching with {}".format(name))
            try:
                users = api.GetUsersSearch(term=name)
                check_for_credentials(users)
            except twitter.error.TwitterError:
                pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="TwitterScraper searches Twitter for user profiles and scrapes any email addresses and phone numbers in their bios. The username and any emails or phone numbers are stored in the SQLite database 'TwitterScraper/users.db'")
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument("-d", "--dictionary", required=True, help="Specify path to a dictionary file to be used for the search queries")
    parser.add_argument("-a", "--analyse", action="store_true", help="Build personality profiles of the users based on their last 200 tweets")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode minimises console output")
    parser.add_argument("--geolocations", action="store_true", help="Scrape geolocations from the user's tweets")
    parser.add_argument("--verified", action="store_true", help="Only select Verified accounts")
    parser.add_argument("--socks5", help="Use a SOCKS5 proxy e.g. --socks5 127.0.0.1:9050")

    args = parser.parse_args()

    proxy_dict = None
    if args.socks5:
        proxy = "socks5://{}".format(args.socks5)
        proxy_dict = {
            'http': proxy,
            'https': proxy
        }

    if "users.db" not in os.listdir():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("""
            CREATE TABLE users (
                username text,
                email text,
                phone text,
                locations text,
                personality text
            )
        """)
    else:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

    api = twitter.Api(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET,
        sleep_on_rate_limit=True,
        proxies=proxy_dict
    )

    scrape_all(api, conn, c, args)
    conn.close()
    print("[*] Results stored in TwitterScraper/users.db")
