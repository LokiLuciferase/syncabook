#!/usr/bin/env python3
import os

from bs4 import BeautifulSoup
import spacy

NLP = None


def _tag_xhtml(in_file: str, out_file: str):
    """Tag the XHTML file with NER tags.

    Args:
        in_file (str): Path to the input XHTML file.
        out_file (str): Path to the output XHTML file.
    """
    global NLP
    if NLP is None:
        NLP = spacy.load('en_core_web_sm')

    with open(in_file, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

    for i, p in enumerate(soup.find_all('p')):
        p_text = p.text
        p.clear()
        sentences = NLP(p_text).sents
        for sentence in sentences:
            span = soup.new_tag('span', **{'id': f'f{i:03}'})
            span.string = sentence.text
            p.append(span)

    with open(out_file, 'w') as f:
        f.write(str(soup))


def tag_xhtmls(in_dir: str, out_dir: str):
    for file_name in os.listdir(in_dir):
        if file_name.endswith('.xhtml'):
            _tag_xhtml(os.path.join(in_dir, file_name), os.path.join(out_dir, file_name))
