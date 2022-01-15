"""
Generates a vocabulary file based on plaintext files defined
in the adjacent sourcelist (sources.txt).
"""

import urllib.request
import sys
import pathlib
import re

SOURCES_PATH = pathlib.Path(pathlib.Path.cwd(), "sources.txt")
DICTIONARY_PATH = pathlib.Path(pathlib.Path.cwd(), "dictionary.txt")

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

    for source in sourcelist:
        response = urllib.request.urlopen(source)
        response_text = response.read().decode()

        for word_candidate in re.split(r"\s", response_text):
            stripped = word_candidate.strip()

            if re.match(r"^[a-zA-Z]{3,}$", stripped):
                words.add(stripped)

    ordered = sorted(list(words))

    with open(DICTIONARY_PATH, "w") as dictionary:
        dictionary.write('\n'.join(ordered))

    print("Dictionary length: %d words" % len(ordered))

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
