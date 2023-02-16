from bs4 import BeautifulSoup
import requests
import phonenumbers
from dataclasses import dataclass
# from selenium import webdriver


########################################################################
# Via class
########################################################################

@dataclass
class Website:
    url: str 
    
    def get_html(self) -> str:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        self.html_source = requests.get(self.url.strip(), headers=headers).text

    # TODO: Improve the format_phones method
    def format_phones(self, phones: list) -> list:
        allowed_characters = [str(x) for x in range(10)]
        allowed_characters += ['(', ')', '+']
        for idx, phone in enumerate(phones):
            phones[idx] = ''.join([char if char in allowed_characters else ' ' for char in phone])

        return phones    


    # TODO: Correct the format_logo method
    def format_logo(self, logo_url: str) -> str:
        if logo_url[:2] == '//':
            return 'https://' + logo_url[2:]
        elif logo_url.startswith('/'):
            logo_url = self.url.split('.com')[0] + logo_url
            return logo_url
        else:
            return logo_url 

    def find_phones(self) -> list:
        # Get matches for USA and BR phone numbers
        phones_br = phonenumbers.PhoneNumberMatcher(self.html_source, "BR")
        phones_usa = phonenumbers.PhoneNumberMatcher(self.html_source, "US")
        phones_br = [phone.raw_string for phone in phones_br]
        phones_usa = [phone.raw_string for phone in phones_usa]
        
        # Join phones
        phones = phones_br + phones_usa 
        
        phones = list(set(phones)) # Exclude duplicates
        self.phones = phones 

    def find_logo(self) -> str:
        soup = BeautifulSoup(self.html_source, 'html.parser')
        # Get all the images from the request
        imgs = soup.find_all('img')
        # Iterate over all images to find logo tags
        # First, check for logo tags on the img src
        for img in imgs:
            # If the source already contains a logo, returns it
            if img['src'].lower().__contains__('logo'):
                self.logo = format_logo(img['src'])
                return 1 
        # Otherwise, check for logo tags on class or alt
        for img in imgs:
            if img.has_attr('data-lazy-src'):    
                continue
            if img.has_attr('class'):
                for desc_class in img['class']:
                    if desc_class.lower().__contains__('logo'):
                        self.logo = format_logo(img['src'])
                        return 1
            if img.has_attr('alt'):
                for desc_alt in img['alt']:
                    if desc_alt.lower().__contains__('logo'):
                        self.logo = format_logo(img['src'])
                        return 1
        self.logo = ''
        return 0

    def parse_infos(self) -> dict:
        self.get_html()
        self.find_logo()
        self.find_phones()
        # Structures the output value
        ret_val = {
            'website': self.url.strip(),
            'phones': self.format_phones(self.phones),
            'logo': self.format_logo(self.logo),
        }

        return ret_val









########################################################################
# Via functions
########################################################################

def format_phones():
    pass

def format_logo(logo_url: str) -> str:
    if logo_url[:2] == '//':
        return 'https://' + logo_url[2:]
    else:
        return logo_url 

def find_phones(source_html: str) -> list:
    # soup = BeautifulSoup(source_html, 'html.parser')
    
    # Get matches for USA and BR phone numbers
    phones_br = phonenumbers.PhoneNumberMatcher(source_html, "BR")
    phones_usa = phonenumbers.PhoneNumberMatcher(source_html, "USA")
    phones_br = [phone.raw_string for phone in phones_br]
    phones_usa = [phone.raw_string for phone in phones_usa]
    
    # Join phones
    phones = phones_br + phones_usa 
    
    phones = list(set(phones)) # Exclude duplicates
    return phones 



def find_logo(source_html: str) -> str:
    soup = BeautifulSoup(source_html, 'html.parser')
    # Get all the images from the request
    imgs = soup.find_all('img')
    # Iterate over all images to find logo tags
    # First, check for logo tags on the img src
    for img in imgs:
        # If the source already contains a logo, returns it
        if img['src'].lower().__contains__('logo'):
            return format_logo(img['src'])
    # Otherwise, check for logo tags on class or alt
    for img in imgs:
        if img.has_attr('class'):
            for desc_class in img['class']:
                if desc_class.lower().__contains__('logo'):
                    return format_logo(img['src'])
        if img.has_attr('alt'):
            for desc_alt in img['alt']:
                if desc_alt.lower().__contains__('logo'):
                    return format_logo(img['src'])
        
def perform_searches(url: str) -> dict:
    ret_val = {
        'website': url
    }
    with_selenium = False
    if with_selenium:
        with webdriver.Chrome('./chromedriver') as browser: 
            browser.get(url)
            # time.sleep(1) - There's no need for sleep on this one
            source_html = browser.page_source
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        source_html = requests.get(url, headers=headers)
        source_html = source_html.text
    ret_val['logo'] = find_logo(source_html)
    ret_val['phones'] = find_phones(source_html)
    print(ret_val)

'''
test0 = 'https://www.cmsenergy.com/contact-us/default.aspx'
test1 = 'https://illion.com.au'
test2 = 'https://illion.com.au/contact-us'
test3 = 'https://www.powerlinx.com/contact'
test4 = 'https://www.cialdnb.com/en'
test5 = 'https://www2.ifsc.usp.br/portal-ifsc/'

print(test0)
perform_searches(test0)

print(test1)
perform_searches(test1)

print(test2)
perform_searches(test2)

print(test3)
perform_searches(test3)

print(test4)
perform_searches(test4)

print(test5)
perform_searches(test5)
'''