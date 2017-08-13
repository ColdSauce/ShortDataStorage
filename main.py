import requests
import sys
import urllib
import http.client
import base64
import argparse

session = requests.Session()

# Write the URL shortener's base URL here:
# For example, stefanaleksic.com/
# Make sure to have the / at the end!
SHORTENER_URL = ""


# I am not going to mention any specific website or service
# in which you can do this. However, you can fork this program
# and manually complete this function to submit an API request
# to some url shortening service.
def get_short_url_from_data(data):
    pass

def _is_redirect(response):
    return response.status//100 == 3 and response.getheader('Location')

def unshorten_url(url, acc):
    if SHORTENER_URL not in url:
        print(url)
        return url
    parsed = urllib.parse.urlparse(url)
    client = http.client.HTTPConnection(parsed.netloc)
    resource = parsed.path
    client.request('HEAD', resource )
    response = client.getresponse()
    if _is_redirect(response):
        acc = response.getheader('Location')

        # The likelyhood of having the link encoded in url safe base64
        # encoded data is so low that I thought I'd take the risk and
        # use this as a way to determine whether the url is just another
        # redirect or one's actual data.
        if SHORTENER_URL not in acc:
            return acc
        else:
            return unshorten_url(response.getheader('Location'), acc)
    else:
        return url

def get_data_from_stdin():
    data = sys.stdin.read()[:-1]
    urlEncodedData = base64.urlsafe_b64encode(data.encode('utf-8'))
    return urlEncodedData.decode('ascii')

def split_string(string, n, acc):
    if len(string) <= n:
        acc.append(string)
        return acc
    acc.append(string[:n])
    return split_string(string[n:], n, acc)

def get_short_urls_from_data(data, segment_size):
    return [get_short_url_from_data(x) 
            for x in split_string(data, segment_size, [])]

def strip_http(url):
    return url[7:]

def get_urls_from_one(root):
    unshortened = strip_http(unshorten_url(root, []))
    acc = []

    for url in unshortened.split('_'):
        acc.append('http://' + SHORTENER_URL + url)
    return acc

def get_data_from_shortened_urls(urls):
    acc = []
    for url in urls:
        unshortened = unshorten_url(url, [])
        stripped_http = strip_http(unshortened)
        decoded = base64.urlsafe_b64decode(stripped_http).decode('utf-8')
        acc.append(decoded)

    return ''.join(acc)

def get_data_after(some_str, target_str):
    return target_str[target_str.find(some_str) + len(some_str):]

def reduce_urls_to_one_url(urls):
    comma_separated_urls = '_'.join(urls)
    minified_urls = '_'.join(get_short_urls_from_data(
        comma_separated_urls, 1000))
    return minified_urls

def main():
    parser = argparse.ArgumentParser(
            description='Save your data in a link shortener!')
    parser.add_argument('urltodecode', nargs='?')
    args = parser.parse_args()
    if args.urltodecode is not None:
        urls = get_urls_from_one(args.urltodecode)
        print(get_data_from_shortened_urls(urls))
    else:
        stdinData = get_data_from_stdin()
        urls  = [get_data_after(SHORTENER_URL, x) 
                for x in get_short_urls_from_data(stdinData, 1000)]
        print(reduce_urls_to_one_url(urls))

if __name__ == '__main__':
    main()


