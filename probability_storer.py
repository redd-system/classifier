#!/usr/bin/env python
# -*- coding: utf-8 -*-

from catenae import Link, Electron, util
from pymongo import MongoClient
from conf import conf_loader as conf


class ProbabilityStorer(Link):

    def setup(self):
        self.mongo_client = MongoClient(conf.mongo['address'], conf.mongo['port'])
        self.db = self.mongo_client.reddit_early_risk
        self.users = self.db.users

        # Ensure users index
        self.users.create_index('nickname', unique=True, background=True)

    def transform(self, electron):
        self.users.update_one(
            { 'nickname': electron.key },
            { '$push': { 'risk_vector': electron.value['proba'] } },
            upsert=True)


if __name__ == '__main__':
    ProbabilityStorer().start(link_mode=Link.CUSTOM_OUTPUT)
