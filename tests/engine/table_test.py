from tests.base_unittest import BaseUnitTest
from nose.tools import *

from pypoker2.engine.card import Card
from pypoker2.engine.pay_info import PayInfo
from pypoker2.engine.action import Action
from pypoker2.engine.player import Player
from pypoker2.engine.table import Table

class TableTest(BaseUnitTest):

  def setUp(self):
    self.__setup_table()
    self.__setup_player()
    self.table.seats.sitdown(self.player)

  def test_reset_deck(self):
    self.table.reset()
    self.eq(52, self.table.deck.size())

  def test_reset_commynity_card(self):
    self.table.reset()
    for card in self.table.deck.draw_cards(5):
      self.table.add_community_card(card)

  def test_reset_player_status(self):
    self.table.reset()
    self.eq(0, len(self.player.hole_card))
    self.eq(0, len(self.player.action_histories))
    self.eq(PayInfo.PAY_TILL_END, self.player.pay_info.status)

  @raises(ValueError)
  def test_community_card_exceed_size(self):
    self.table.add_community_card(Card.from_id(1))

  def test_shift_dealer_btn_skip(self):
    table = self.__setup_players_with_table()
    table.shift_dealer_btn()
    self.eq(2, table.dealer_btn)
    table.shift_dealer_btn()
    self.eq(0, table.dealer_btn)


  def __setup_table(self):
    self.table = Table()
    for card in self.table.deck.draw_cards(5):
      self.table.add_community_card(card)

  def __setup_player(self):
    self.player = Player("uuid", 100)
    self.player.add_holecard([Card.from_id(cid+1) for cid in range(2)])
    self.player.add_action_history(Action.CALL, 10)
    self.player.pay_info.update_to_fold()

  def __setup_players_with_table(self):
    p1 = Player("uuid1", 100)
    p2 = Player("uuid2", 100)
    p3 = Player("uuid3", 100)
    p2.pay_info.update_to_fold()
    p3.pay_info.update_to_allin()
    table = Table()
    for player in [p1, p2, p3]:
      table.seats.sitdown(player)
    return table
