#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800.

Writes a single sentence (at most 200 characters) explaining the modern
internet to a time traveler from 1800, using only words that already
existed before 1800. Stdlib only.

Gate (from the kit's competition.yaml): /output/entry.txt must be UTF-8
text of 1 to 200 characters, not only white space.
"""

import os
import re
import sys

# The entry: one sentence, built only from things a person from 1800
# already knows -- a library, a post house, copper threads, a letter,
# a candle -- to picture instant writing across the sea and all the
# world's books standing open at once.
SENTENCE = (
    "Every town shares one great library and post house, joined by "
    "copper threads, so a letter writ in London is read in Boston "
    "ere thy candle burns low."
)

# Words coined after 1800 that must never appear in the entry.
BLOCKLIST = frozenset(
    [
        "internet",
        "computer",
        "screen",
        "digital",
        "online",
        "website",
        "email",
        "phone",
        "telephone",
        "telegraph",
        "app",
        "video",
        "software",
        "server",
        "cloud",
        "pixel",
        "browser",
        "chat",
        "download",
        "upload",
        "wifi",
        "link",
        "click",
        "data",
        "code",
        "virtual",
        "cyber",
        "electronic",
    ]
)


def words_of(text):
    """Lower-cased words of *text*, stripped of punctuation."""
    return re.findall(r"[a-z]+", text.lower())


def validate(text):
    """Raise ValueError unless *text* passes every gate the kit sets."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) != len(text.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "entry must be 1 to 200 characters, got %d" % len(text)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    # Exactly one sentence: one terminal full stop, no other
    # sentence-ending punctuation anywhere.
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in '.'")
    if any(mark in text for mark in ("!", "?", ";", ":")):
        raise ValueError("entry must be exactly one sentence")
    banned = sorted(set(words_of(text)) & BLOCKLIST)
    if banned:
        raise ValueError("entry uses words coined after 1800: %s" % banned)
    return text


def main():
    text = validate(SENTENCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts every character.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    print("wrote %s (%d characters)" % (out_path, len(text)))


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
