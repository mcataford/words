# words
📚 A better curated wordlist

I love word puzzles and often find myself needing a wordlist to make my own. Wordlists are apparently hard and the
ones out there don't cut it. To put an end to this endless anguish, I've just decided to publish my own.

The wordlist is built from great works pulled from [Project Gutenberg](https://www.gutenberg.org).

## Usage

To add sources to the sourcelist, use `python cli.py add <url>`. The URL should lead to plain text file containing your
source text. 

You can build the dictionary via `python cli.py build` -- the resulting `dictionary.txt` will contain unique lowercased
words of three or more characters extracted from the materials specified in the sourcelist.
