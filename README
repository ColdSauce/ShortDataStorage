# URL Shortener As a Data Store

A URL shortening service, in the most basic sense, is just a map from short URL to long URL and vice versa. Most URL shorteners don’t do anything to see if the URLs are actually real. This means that arbitrary data can be stored in the URLs and later retrieved. 

This repo contains a PoC of storing and later retreiving data from most URL shortening services. I have explicitly made it so that it is URL Shortening service agnostic. If you'd like to use a URL shortening service to do this, you have to explicitly call their API and so on.

If you'd like to store data, you can pipe it to stdin to the program which will generate a short link when you have correctly hooked up the URL shortening service you would like to use.

`cat somefile.html | python main.py`

If you'd like to get data from a specific shortened URL, you can explicitly pass it in as a command line argument.

`python main.py <some shortened URL> > file_to_save_data_to.bin`

To save data to a URL shortening service, this code encodes all the data in URL Safe Base64, splits it into batched chunks, calls the URL shortening service's API with a url `http://<the base 64 encoded chunk` which the URL shortening service takes in no problem. The service returns a shortened URL for the data. Then, all of these shortened URLS that were generated are compiled into a string that separates them with `_` underscores. This string is then itself shortened and from that, one
shortened URL is generated. 

The way to get the data back is basically the process just described but in reverse. 

The reason I did this was because I was bored.
