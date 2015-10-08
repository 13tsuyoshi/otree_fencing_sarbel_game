# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass

class Anticipate(Page):
    form_model = models.Player
    form_fields = ['anticipation']
    
    def vars_for_all_templates(self):
        return {'player1_skills':Constants.first_good_skill
                'player2_skills':Constants.second_good_skil
                'round_number': self.subsession.round_number,
                'role': self.player.role()}　　#models.pyのrole
#timeout_seconds = 20
#timeout_submission = {'accept': True}これらで時間制約がつけられるかもしれないhttp://otree.readthedocs.org/en/latest/views.htmlより


class Action(Page):
    form_model = models.Player
    form_fields = ['action']




class ResultsWaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        self.play.set_payoffs()#利得がplayに書かれているので


class Results(Page):
    
    def vars_for_template(self): #prisonor参照
        player_in_all_rounds = self.player.in_all_rounds()
        own_total_payoff = sum([p.payoff for p in player_in_all_rounds])
        opponent_total_payoff = sum([p.other_player().payoff for p in player_in_all_rounds])
        
        return {'player_in_all_rounds': player_in_all_rounds,
                'own_total_payoff':own_total_payoff
                'opponent_total_payoff':opponent_total_payoff
                'round_number': self.subsession.round_number,
                'end_game_point':Constants.end_game_point}
#'player_in_previous_rounds': self.player.in_previous_rounds(),



page_sequence = [
        Anticipate,
        ResultsWaitPage,
        Action,
        ResultsWaitPage,
        Results
    ]
