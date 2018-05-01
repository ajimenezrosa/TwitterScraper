import sqlite3
import twitter
import re, os, sys

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""

def scrape_all(api, conn, c, name_dictionary):

    def check_for_credentials(users):
        for user in users:
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


    with open(name_dictionary, 'r') as names:
        for name in names:
            print("Searching with {}".format(name))
            users = api.GetUsersSearch(term=name)
            check_for_credentials(users)


if __name__ == "__main__":
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
        proxies=None
    )

    name_dictionary = "combined.dic"

    scrape_all(api, conn, c, name_dictionary)
    conn.close()
