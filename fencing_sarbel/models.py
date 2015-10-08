# -*- coding: utf-8 -*-
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

author = 'tsuyoshi'

doc = """
    Your app description
    """


class Constants(BaseConstants):
    name_in_url = 'fencing_sarbel'#長いとエラーを起こすので注意
    players_per_group = 2
    num_rounds = 30 #15点でおわらせるにはどうすればよいかが課題
    
    # define more constants here
    point = c(0.5)#floatで大丈夫か要チェック
    non_point = c(0)
    end_game_point = c(15)
    first_good_skill = {'attack':random.random(),'repost':random.random(),'back':random.random()}#ここの値って毎回変わらないよね？
    second_good_skill = {'attack':random.random(),'repost':random.random(),'back':random.random()}

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
# </built-in>


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
        if self.id_in_group == 1:
            return 'Player 1'
        if self.id_in_group == 2:
            return 'Player 2'

    action = models.CharField(choices=['attack', 'repost','back'],widget=widgets.RadioSelect())
    anticipation = models.CharField(choices=['attack', 'repost','back'],widget=widgets.RadioSelect())
    
    def set_payoff(self): #こうすると２点ずつ入んない？→０．５×２にすればいい。その時は
        if (self.action == 'repost' or　'back')and (self.other_player().anticipation == 'repost' or 'back'):
            self.payoff = Constants.non_point    #直接c(0)ってやってはいけないのか
            self.other_player().payoff = Constants.non_point
        elif self.action == self.other_player().anticipation and self.other_player().action != self.anticipation:
            self.payoff = Constants.non_point
            self.other_player().payoff = Constants.point
        elif　self.other_player().action == self.anticipation and self.action != self.other_player().anticipation:
            self.payoff = Constants.point
            self.other_player().payoff = Constants.non_point
        elif (self.action == self.other_player().anticipation and self.other_player().action == self.anticipation) or (self.action != self.other_player().anticipation and self.other_player().action != self.anticipation):
            if self.id_in_group ==1:#player１なら
                own_good_skill = Constants.first_good_skill
                other_player_good_skill = Constants.second_good_skill
            if self.id_in_group ==2:#player2なら
                own_player_good_skill = Constants.second_good_skill
                other_player_good_skill = Constants.first_good_skill
            if own_good_skill[self.action] >  other_player_good_skill[self.other_player().action ]:#self.actionは文字列で返される？
                self.payoff = Constants.point
                self.other_player().payoff = Constants.non_point
            elif own_good_skill[self.action] <  other_player_good_skill[self.other_player().action ]:
                self.payoff = Constants.non_point
                self.other_player().payoff = Constants.point
            elif own_good_skill[self.action] ==  other_player_good_skill[self.other_player().action ]:
                self.payoff = Constants.non_point
                self.other_player().payoff = Constants.non_point




