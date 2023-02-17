import string
from dataclasses import dataclass
import urllib

import phonenumbers
import requests
from bs4 import BeautifulSoup



@dataclass
class Website:
    url: str 
    
    def get_html(self) -> str:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        try:
            response = requests.get(self.url, headers=headers)
            # response.raise_for_status()
            self.html_source = response.text
            return True
        except Exception as e:
            print(e)
            return False

    def clean_phone(self, phone_number):
        allowed_characters = string.digits
        allowed_characters += '()+'
        return ''.join([char if char in allowed_characters else ' ' for char in phone_number])

    
    def format_phones(self, phones: list) -> list:
        return [self.clean_phone(phone_number) for phone_number in phones]
        
    def format_logo(self, logo_url: str) -> str:
        url_splitted = urllib.parse.urlsplit(self.url)
        if logo_url[:2] == '//':
            return f'{url_splitted.scheme}:{logo_url}'
        elif logo_url.startswith('/'):
            return f'{url_splitted.scheme}://{url_splitted.hostname}{logo_url}'
        else:
            return logo_url 

    # TODO: Add EU phones
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
            if 'logo' in img['src'].lower():
                self.logo = self.format_logo(img['src'])
                return True 
        # Otherwise, check for logo tags on class or alt
        for img in imgs:
            # I'm skipping lazy loaded images
            if img.has_attr('data-lazy-src'):    
                continue
            if img.has_attr('class'):
                for desc_class in img['class']:
                    if 'logo' in desc_class.lower():
                        self.logo = self.format_logo(img['src'])
                        return True
            if img.has_attr('alt'):
                for desc_alt in img['alt']:
                    if 'logo' in desc_alt.lower():
                        self.logo = self.format_logo(img['src'])
                        return True
        self.logo = ''
        return False

    def parse_infos(self) -> dict:
        if not self.get_html():
            return {}
        self.find_logo()
        self.find_phones()
        # Structures the output value
        ret_val = {
            'website': self.url.strip(),
            'phones': self.format_phones(self.phones),
            'logo': self.format_logo(self.logo),
        }

        return ret_val

