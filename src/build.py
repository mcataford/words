"""
Generates a vocabulary file based on plaintext files defined
in the adjacent sourcelist (sources.txt).
"""

import urllib.request
import pathlib
import re
import logging

SOURCES_PATH = pathlib.Path(pathlib.Path.cwd(), "sources.txt")
FULL_DICTIONARY_PATH = pathlib.Path(pathlib.Path.cwd(), "dictionary_full.txt")
COMMON_DICTIONARY_PATH = pathlib.Path(pathlib.Path.cwd(), "dictionary_common.txt")

COMMON_FREQUENCY_THRESHHOLD = 5

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

    logger.info("Fetching from %d sources" % len(sourcelist))

    words_by_count = {}

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
            normalized = word_candidate.strip().lower()

            if re.match(r"^[a-z]{3,}$", normalized):
                words_by_count[normalized] = words_by_count.get(normalized, 0) + 1

    full_dictionary = set()
    common_dictionary = set()

    for word, count in words_by_count.items():
        if count >= COMMON_FREQUENCY_THRESHHOLD:
            common_dictionary.add(word)

        full_dictionary.add(word)

    with open(FULL_DICTIONARY_PATH, "w") as dictionary:
        dictionary.write('\n'.join(sorted(list(full_dictionary))))
    
    with open(COMMON_DICTIONARY_PATH, "w") as dictionary:
        dictionary.write('\n'.join(sorted(list(common_dictionary))))

    logger.info("Full dictionary length: %d words" % len(full_dictionary))
    logger.info("Common words dictionary length: %d words" % len(common_dictionary))
    
if __name__ == "__main__":
    build_from_sources()
