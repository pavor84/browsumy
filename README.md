Simple django-based web service for summarization using [Sumy](https://github.com/miso-belica/sumy) library.
Automatically detects language for provided document url and returns plain text with summarized content.
Supported language set is manually restricted to [English, Russian].

**Installation:**

apt-get install python python-dev python-setuptools
apt-get install libxml2-dev libxslt1-dev zlib1g-dev

easy_install pip

pip install sumy
pip install langid
pip install Django==1.9.7

python -c "import nltk; nltk.download('punkt')"

python -c "import nltk; nltk.download('stopwords')"

Stopwords for some other languages for Sumy can be found in [PyTeaser](https://github.com/xiaoxu193/PyTeaser)).
Just put them to sumy/data/stopwords directory.

You might also need additional .pickle punctuation files for ntlk, they can be found in (https://github.com/mhq/train_punkt) repository.
Put them to ntlk_data/tokenizers/punkt directory.

**Example usage:**

http://<hostname>/sumapi/sum/?method=lsa&length=10%25&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAutomatic_summarization

GET parameters:
- method can be one of the following: luhn, edmundson, lsa, text-rank, lex-rank, sum-basic, kl
- length defines number of sentences or percentage of the original text
- url of html document to summarize

Returned result: plain/text with sentences, Content-Language header contains autodetected language.
