#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib
from collections import defaultdict
from math import log10, floor
from collections import OrderedDict


NGRAM_API_URI = "https://{0}.linggle.com/query/"
EXP_API_URI = "https://{0}.linggle.com/example/"


class Linggle:
    def __init__(self, ver='www'):
        self.ver = ver

    def __getitem__(self, query):
        return self.search(query)

    def search(self, query):
        query = query.replace('/', '@')
        query = urllib.parse.quote(query, safe='')
        req = requests.get(NGRAM_API_URI.format(self.ver) + query)
        results = req.json()
        return results.get("ngrams", [])

    def get_example(self, ngram_str):
        res = requests.post(EXP_API_URI.format(
            self.ver), json={'ngram': ngram_str})
        if res.status_code == 200:
            result = res.json()
            return result.get("examples", [])
        return []


if __name__ == "__main__":
    ling = Linggle('www')

