# CIAL dun&bradstreet Technical Assignment

## Introduction

On this assignment, the application receives various URLs and scrap them, searching
for phone numbers and its logo. 

## Instalation

To run the application, first run the command

```
docker build -t cial_assignment .
```

After that, one can run the program, passing standard
inputs to the application, via

```
cat websites.txt | docker run -i cial_assignment
```

Another way to run the code locally would be through the steps

```
pip install -r requirements.txt
cat websites.txt | python -m main
```

Note, however, that to run the program this way, we recommend
that the user creates a virtual environment beforehand.

## Technical commentaries

First, I dealed with the logo feature. My main idea was to extract, via the 3rd party library `BeautifulSoup`,
all the images in the html source code and then look for `logo` tags in them. This strategy ended up being
effective and was left as the final strategy for obtaining the logos.

The second part, extract the phones, is more tricky. This is because dealing with regex to extract phone can be
extremely complicated and lead to errors. Thus, a solution was to use the Google library `phonenumbers`, which
find phone format matches on a given text (since we specify which country format it needs to look for). 

Another comment is that one can trackle this problem using the `selenium` library. With this strategy, one can
search for logos and phones which do not appear in the standard request used here. However, the application
gets significantly slower with this approach, and I chose to follow with the `requests` library.