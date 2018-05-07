#!/usr/bin/python3
import sqlite3
import twitter
import argparse
import re, os, sys

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""

def scrape_all(api, conn, c, args):

    name_dictionary = args.dictionary

    def check_for_credentials(users):
        def check():
            c.execute("SELECT COUNT(*) FROM users WHERE username=?", (user.screen_name,))
            occurences = c.fetchone()[0]
            if not occurences:
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', user.description)
                phones = re.findall("[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}", user.description)
                if emails or phones:
                    c.execute("INSERT INTO users ('username') VALUES (?)", (user.screen_name,))
                    conn.commit()
                if emails:
                    for email in emails:
                        print("[\033[92mFOUND\033[0m] Email for @{}: {}".format(user.screen_name, email))
                    c.execute("UPDATE users SET email=? WHERE username=?", (str(emails), user.screen_name))
                    conn.commit()
                if phones:
                    for phone in phones:
                        print("[\033[92mFOUND\033[0m] Phone for @{}: {}".format(user.screen_name, phone))
                    c.execute("UPDATE users SET phone=? WHERE username=?", (str(phones), user.screen_name))
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
            users = api.GetUsersSearch(term=name)
            check_for_credentials(users)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="TwitterScraper searches Twitter for user profiles and scrapes any email addresses and phone numbers in their bios. The username and any emails or phone numbers are stored in the SQLite database 'TwitterScraper/users.db'")
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument("-d", "--dictionary", required=True, help="Specify path to a dictionary file to be used for the search queries")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode minimises console output")
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
                phone text
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
