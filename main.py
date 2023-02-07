#!/usr/bin/env python

from passage import Passage
from typing import List

if __name__ == '__main__':
    passage = Passage(open("api-key.txt", "r").read())
    print(passage.get_passage_esv("Genesis 1-3"))
