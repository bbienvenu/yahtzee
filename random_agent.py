import utils
from yahtzee_agent import YahtzeeAgent

class RandomAgent(YahtzeeAgent):
    """Agent that plays randomly."""

    def __init__(self, name="random"):
        super().__init__(name)

    def roll_dice(self, dice_values, nrolls)->list:
        return utils.random_dice_to_roll()

    def choose_decision(self, dice_values)->str:
        return utils.arbitraty_decision(dice_values, self.scorecard)
