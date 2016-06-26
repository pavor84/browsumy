# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from langid.langid import LanguageIdentifier, model

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import fetch_url, get_stop_words, ItemsCount

SUMY_LANGUAGES = {
    "en": "english",
    "ru": "russian",
}

AVAILABLE_METHODS = {
    "luhn": LuhnSummarizer,
    "edmundson": EdmundsonSummarizer,
    "lsa": LsaSummarizer,
    "text-rank": TextRankSummarizer,
    "lex-rank": LexRankSummarizer,
    "sum-basic": SumBasicSummarizer,
    "kl": KLSummarizer,
}


def detect_language(html_content):
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    identifier.set_languages(SUMY_LANGUAGES.keys())
    iso_lang, _ = identifier.classify(html_content)
    return iso_lang


def build_summarizer(summarizer_class, stop_words, stemmer, parser):
    summarizer = summarizer_class(stemmer)
    if summarizer_class is EdmundsonSummarizer:
        summarizer.null_words = stop_words
        summarizer.bonus_words = parser.significant_words
        summarizer.stigma_words = parser.stigma_words
    else:
        summarizer.stop_words = stop_words
    return summarizer


def summarize(method, length, url):
    html_content = fetch_url(url)
    iso_lang = detect_language(html_content)
    language = SUMY_LANGUAGES[iso_lang]
    stemmer = Stemmer(language)
    parser = HtmlParser.from_string(html_content, url, Tokenizer(language))

    summarizer_class = AVAILABLE_METHODS[method]
    summarizer = build_summarizer(summarizer_class, get_stop_words(language), stemmer, parser)

    sentences = summarizer(parser.document, ItemsCount(length))
    summary = ' '.join([unicode(sentence) for sentence in sentences])
    return summary, iso_lang
