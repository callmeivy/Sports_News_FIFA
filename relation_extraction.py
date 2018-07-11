# -*- coding: UTF-8 -*-
import re
import nltk
def open_ie():
    PR = re.compile(r'.*\president\b')
    for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
        for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern=PR):
            print nltk.sem.rtuple(rel)

if __name__ == "__main__":
    open_ie()