# TwitterScraper
This bot can be used to search Twitter for email addresses and phone numbers left in users' bios. The results are stored in a SQLite database. 

## Usage
```
[joe@centos TwitterScraper]$ ./twitter-scraper.py --help
usage: twitter-scraper.py [-h] -d DICTIONARY [-q] [--socks5 SOCKS5]

TwitterScraper searches Twitter for profiles and scrapes any email addresses
and phone numbers left in a user's bio.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Quiet mode minimises console output
  --socks5 SOCKS5       Use a SOCKS5 proxy e.g. --socks5 127.0.0.1:9050

required arguments:
  -d DICTIONARY, --dictionary DICTIONARY
                        Specify path to a dictionary file to be used for the
                        search queries

```
The program requires a dictionary file for the search terms. This can be any file with a each search term on its own line. I have provided an ordered list of over 20,000 first names in the namelist.dic file.

You may also specify a SOCKS5 proxy to use. For example, with Tor:
```
./twitter-scraper.py -d namelist.dic --socks5 127.0.0.1:9050
```
## Getting started

To access the Twitter API, you will need to obtain API keys for the account you want to use. Head over to the [Twitter developers](https://developer.twitter.com/) site and get your access token key & secret and a consumer key & secret.

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
