import http
import sys
import threading

from tools import Website


def main(url: str) -> None:
    '''
    This function creates a Website class and 
    gets all the information needed.
    '''
    website_infos, status = Website(url).parse_infos()
    print(website_infos)
    if status >= 400:
        print(f'{status} - {http.client.responses[status]}')



if __name__ == '__main__':
    # With threading, iterate over all urls
    for url in sys.stdin:
        if url.strip(): # Guarantees that no empty lines will enter the loop
            threading.Thread(target=main, args=(url.strip(),)).start()
        else:
            continue
        


    
    