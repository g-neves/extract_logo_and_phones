import string
import urllib
from dataclasses import dataclass
from typing import List, Tuple

import phonenumbers
import requests
from bs4 import BeautifulSoup



@dataclass
class Website:
    url: str 
    
    def get_html(self) -> str:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        try:
            self.response = requests.get(self.url, headers=headers)
            # response.raise_for_status()
            self.html_source = self.response.text
            return True
        except Exception as e:
            print(f'Error with url {self.url}: {e}')
            return False

    def clean_phone(self, phone_number: str) -> str:
        # Clean the phone number, letting only
        # the allowed symbols
        allowed_characters = string.digits
        allowed_characters += '()+'
        return ''.join([char if char in allowed_characters else ' ' for char in phone_number])

    def format_phones(self, phones: List[str]) -> List[str]:
        # Formats to let only the allowed symbols
        return [self.clean_phone(phone_number) for phone_number in phones]
        
    def format_logo(self, logo_url: str) -> str:
        # Corrects the logo path to get the absolute path.
        url_splitted = urllib.parse.urlsplit(self.url)
        if logo_url[:2] == '//':
            return f'{url_splitted.scheme}:{logo_url}'
        elif logo_url.startswith('/'):
            return f'{url_splitted.scheme}://{url_splitted.hostname}{logo_url}'
        else:
            return logo_url 

    def find_phones(self) -> List[str]:
        # Get matches for USA, Brazil and Great Britain phone numbers
        # This scope can be enlarged, of course. To keep things simple,
        # right now I chose to keep these 3 countries.
        # OBS: Germany enhance considerably the number of found phones.
        phones = []
        for country in ["BR", "US", "GB"]:
            phones_match = phonenumbers.PhoneNumberMatcher(self.html_source, country)
            phones += [phone.raw_string for phone in phones_match]
        
        phones = list(set(phones)) # Exclude duplicates
        self.phones = phones 

    def find_logo(self) -> bool:
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
            # Now, if the tag appears in the class or alt
            # of a img, I get the image source.
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

    def parse_infos(self) -> Tuple[dict, int]:
        if not self.get_html():
            ret_val = {
                'website': self.url.strip(),
                'phones': [],
                'logo': ''
            }
            return ret_val, -1
        self.find_logo()
        self.find_phones()
        # Structures the output value
        ret_val = {
            'website': self.url.strip(),
            'phones': self.format_phones(self.phones),
            'logo': self.format_logo(self.logo),
        }

        return ret_val, self.response.status_code

