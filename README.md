# TwitterScraper
This bot can be used to scrape Twitter for email addresses, geolocations and phone numbers associated with user accounts. Additionally, it can use AI to build profiles about those users' personalities including their values and needs. The results are stored in a SQLite database.

## Usage
```
[joe@centos TwitterScraper]$ ./twitter-scraper.py --help
usage: twitter-scraper.py [-h] -d DICTIONARY [-a] [-q] [--geolocations]
                          [--verified] [--socks5 SOCKS5]

TwitterScraper searches Twitter for user profiles and scrapes any email
addresses and phone numbers in their bios. The username and any emails or
phone numbers are stored in the SQLite database 'TwitterScraper/users.db'

optional arguments:
  -h, --help            show this help message and exit
  -a, --analyse         Build personality profiles of the users based on their
                        last 200 tweets
  -q, --quiet           Quiet mode minimises console output
  --geolocations        Scrape geolocations from the user's tweets
  --verified            Only select Verified accounts
  --socks5 SOCKS5       Use a SOCKS5 proxy e.g. --socks5 127.0.0.1:9050

required arguments:
  -d DICTIONARY, --dictionary DICTIONARY
                        Specify path to a dictionary file to be used for the
                        search queries

```
The program requires a dictionary file for the search terms. This can be any file with each search term on its own line. I have provided an ordered list of over 20,000 first names in the namelist.dic file.

You may also specify a SOCKS5 proxy to use. For example, with Tor:
```
./twitter-scraper.py -d namelist.dic --socks5 127.0.0.1:9050
```
## Getting started

To access the Twitter API, you will need to obtain API keys for the account you want to use. Head over to the [Twitter API](https://apps.twitter.com/) site and create an app.

Next you will need to input the keys into the source code.
```
vim twitter-scraper.py
```
<pre>
...
CONSUMER_KEY = "<b>your consumer key</b>"
CONSUMER_SECRET = "<b>your consumer secret</b>"
ACCESS_TOKEN_KEY = "<b>your access key</b>"
ACCESS_TOKEN_SECRET = "<b>your access secret</b>"
...
</pre>
If you haven't already, install the dependencies.
```
sudo pip3 install -r requirements.txt
```
Then run the script, specifying a dictionary file to use.
```
python3 twitter-scraper.py -d namelist.dic
```

## Optional: IBM Watson API

You can use the Watson Personality Insights API to build profiles about the users. You will need a [Bluemix](https://bluemix.net) account. After creating an account, create a new resource from your dashboard and select the Personality Insights from the Watson platform. Once you've created the new service, get your API credentials and add them to the source.
```
vim twitter-scraper.py
```
<pre>
...
USERNAME = "<b>username</b>"
PASSWORD = "<b>password</b>"
...
</pre>
