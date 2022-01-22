# words
📚 A better curated wordlist

I love word puzzles and often find myself needing a wordlist to make my own. Wordlists are apparently hard and the
ones out there don't cut it. To put an end to this endless anguish, I've just decided to publish my own.

The wordlist is built from great works pulled from [Project Gutenberg](https://www.gutenberg.org).

## Usage

You can build the dictionaries via `python src/build.py`. This will pull the remote sources specified in `sources.txt`
and will build the different dictionaries:

- The full dictionary (`dictionary_full.txt`) contains all words that contain at least three letters extracted from the
  source material;
- The common words dictionary (`dictionary_common.txt`) contains words that appear at least 5 times in the source
  material;
