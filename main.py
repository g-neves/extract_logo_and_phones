import sys
import threading

from tools import Website



def main(url: str) -> None:
    '''
    This function creates a Website class and 
    gets all the information needed.
    '''
    print(Website(url).parse_infos())



if __name__ == '__main__':
    # With threading, iterate over all urls
    for url in sys.stdin:
        if url.strip():
            threading.Thread(target=main, args=(url.strip(),)).start()
        


    
    