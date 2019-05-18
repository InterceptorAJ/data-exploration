#! env/bin/python

import html2text
import nltk
import csv

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import digits

# Use following statment at the first run.
nltk.download()

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

documents_content = []

f = open('1.html', 'r')
content = f.read()
divider = 'KONIEC'
documents = content.split(divider)


i = 0
for document in documents:
    print(i)
    i += 1

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = False
    text = text_maker.handle(document)
    title = text.split('\n', 1)[0]

    text = text.replace('\n', '')

    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', ':', ';', '|', '[', ']', '"', '/', 'https://']

    for char in special_characters:
        text = text.replace(char, ' ')
        title = title.replace(char, '')

    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    text = text.replace('  ', ' ')
    text = text.replace('\t', '')
    title = title.replace('arXiv', '')
    # title = title.replace(' ', '_')


    # word_tokens = word_tokenize(text)
    # filtered_sentence = [w for w in word_tokens if not w in stop_words]
    # filtered_sentence = ' '.join(filtered_sentence)

    title = title[:50]
    title += str(i)
    documents_content.append([title, text])

with open('res.csv', mode='w') as f:
    writer = csv.writer(
        f,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    id = 1

    keys = ['title', 'content']
    writer.writerow(keys)

    for doc in documents_content:

        writer.writerow(doc)

with open('pages.arff', mode='w') as f:
    s = "@relation dokumenty\n@attribute _title string\n@attribute content string\n@data\n"
    i = 1
    for title, content in documents_content:
        t = '"{}","{}"\n'.format(title, content)
        i += 1
        s += t

    s = s[:-1]

    f.write(s)
