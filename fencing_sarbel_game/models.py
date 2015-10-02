# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'tsuyoshi'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'fencing_sarbel_game'#長いとエラーを起こすので注意
    players_per_group = 2
    num_rounds = 100 #Variable number of roundsIf you want a variable number of rounds, consider setting num_rounds to some high number, and then in your app, conditionally hide the {% next_button %} element, so that the user cannot proceed to the next page.より高めに設定。　　15点でおわらせるにはどうすればよいか。
    # define more constants here
    point = c(1)
    good_skill = [[[0.5],[0.3],[0.7]],[[0.5],[0.7],[0.3]]]#ここはいつかrandom変数にする

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        
        if p1.action == 'attack' and p2.anticipation == 'attack' and p1.action == 'attack' and p2.anticipation == 'attack':
            possibility =  random.uniform(0, 1)#もっと簡潔な方法がある はず。
            if 0 <= possibility <0.1:
                p1.payoff += Constants.point
            if 0.1 <= possibility =<0.8:
                pass
            if 0.8 < possibility =<0.1:
                p2.payoff += Constants.point  #これらの条件式をたくさん書く


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    def role(self):
        # you can make this depend of self.id_in_group
        return Constants.good_skill[self.id_in_group - 1]#選択画面に得意技を出させるためのもの

    action = models.CharField(choices=['attack', 'repost','back'],widget=widgets.RadioSelect())#何の行動をとるか選択　In views.py, define the Choice page like form_fields = ['action']
    anticipation = models.CharField(choices=['attack', 'repost','back'],widget=widgets.RadioSelect())


