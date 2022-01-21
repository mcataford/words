"""
Generates a vocabulary file based on plaintext files defined
in the adjacent sourcelist (sources.txt).
"""

import urllib.request
import sys
import pathlib
import re
import logging

SOURCES_PATH = pathlib.Path(pathlib.Path.cwd(), "sources.txt")
DICTIONARY_PATH = pathlib.Path(pathlib.Path.cwd(), "dictionary.txt")

logger = logging.getLogger('words-cli')
logging.basicConfig(level=logging.INFO)


def build_from_sources():
    """
    Pulls each resource from the sourcelist, tokenizes its contents
    and aggregates unique words of 3 or more characters. The
    resulting set of words is persisted to `dictionary.txt` in the
    current working directory.
    """

    with open(SOURCES_PATH, "r") as sources:
        sourcelist = [source.strip() for source in sources.read().split('\n') if source]

    words = set()

    logger.info("Fetching from %d sources" % len(sourcelist))

    for source in sourcelist:
        logger.info("Fetching from %s..." % source)
        response = urllib.request.urlopen(source)
 
        raw_response = response.read()

        # Decode if UTF8.
        try:
            response_text = raw_response.decode()
        except Exception as e:
            response_text = str(raw_response)

        for word_candidate in re.split(r"\s", response_text):
            stripped = word_candidate.strip().lower()

            if re.match(r"^[a-z]{3,}$", stripped):
                words.add(stripped)

    ordered = sorted(list(words))

    with open(DICTIONARY_PATH, "w") as dictionary:
        dictionary.write('\n'.join(ordered))

    logger.info("Dictionary length: %d words" % len(ordered))

def add_to_sources(url: str):
    """
    Adds a new resource to the sourcelist. The entries are assumed to be
    valid URLs pointing to plaintext files.
    """

    with open(SOURCES_PATH, "a") as sources:
        sources.write(url + "\n")

if __name__ == "__main__":
    """
    Commands:
        add <url>
            Adds the given URL to the sourcelist.
        build
            Builds a dictionary of unique words from the sourcelist resources.
    """
    args = sys.argv[1:]

    if len(args) < 1:
        raise Exception("Missing options")

    action = args[0]

    if action == "add" and len(args) == 2:
        add_to_sources(args[1])

    elif action == "build":
        build_from_sources()
