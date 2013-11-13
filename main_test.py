# -*- coding: utf-8 -*-
__author__ = 'modulus'

from unittest import TestCase
from addon_new import createMainMenu, createSubMenu
from utils import Utils


class MainTest(TestCase):

    def test_VerifyMainMenuUrls(self):
        shows = createMainMenu("http://dbtv.no/", None)

        for show in shows:
            self.assertEquals(1, Utils.checkURL(show.url), "Could not find url "+show.url)
            self.assertTrue(show.title, "Serie has no title")

    def test_VerifySubMenuUrls(self):
        shows = createMainMenu("http://dbtv.no", None)
        all_episodes = []
        for show in shows:
            episodes = createSubMenu("http://dbtv.no", show.title, None, None)
            self.assertTrue(episodes)
            all_episodes.append(episodes)
        self.assertTrue(all_episodes)


