# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass

class Choice(Page):

    form_model = models.Player   #models.pyのPlayerクラスに選択の行動が入っているので
    form_fields = ['action']     #'action'と'anticipation'の二つを表示させたいんだけどどうしよう？

    def vars_for_template(self):  #まだよくわからないポイント
        return {'player_in_previous_rounds': self.player.in_previous_rounds(),}

	




class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()#利得がグループに書かれているので


class Results(Page):
    pass
　　　
    #for p in self.get_players():
        #p.payoff = Constants.endowment - p.contribution + self.individual_share

page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
