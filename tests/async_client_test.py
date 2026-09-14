# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import asyncio

import vcr
from unittest import TestCase

from contentful.async_client import AsyncClient
from contentful.content_type_cache import ContentTypeCache


class AsyncClientTest(TestCase):
    def setUp(self):
        ContentTypeCache.__CACHE__ = {}

    @vcr.use_cassette('fixtures/client/entry.yaml', decode_compressed_response=True)
    def test_async_client_entry(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entry = asyncio.run(client.entry('nyancat'))

        self.assertEqual(str(entry), "<Entry[cat] id='nyancat'>")
        self.assertEqual(str(entry.best_friend), "<Entry[cat] id='happycat'>")

    @vcr.use_cassette('fixtures/client/entries.yaml', decode_compressed_response=True)
    def test_async_client_entries(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entries = asyncio.run(client.entries())

        self.assertTrue(len(entries) > 0)
