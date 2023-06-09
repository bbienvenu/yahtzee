import random
import utils
import time
from yahtzee_agent import YahtzeeAgent

class Game:
    """Class to manage a game of Yahtzee between two agents."""

    def __init__(self, agent1: YahtzeeAgent, agent2: YahtzeeAgent):
        self.agents = [agent1, agent2]
        self.current_agent_index = 0
        self.dice_values = list()
        self.remaining_rolls = 3

    def play(self):
        """Plays a game of Yahtzee between two agents."""
        self.agents[0].scorecard = utils.BLANK_SCORECARD.copy()
        self.agents[0].opponent_scorecard = utils.BLANK_SCORECARD.copy()
        self.agents[1].scorecard = utils.BLANK_SCORECARD.copy()
        self.agents[1].opponent_scorecard = utils.BLANK_SCORECARD.copy()

        for i in range(2 * utils.N_TURNS):

            self.dice_values = [random.randint(1, utils.N_FACES) for _ in range(utils.N_DICE)]
            self.remaining_rolls = 2

            while self.remaining_rolls > 0:
                dice_to_roll = self.agents[self.current_agent_index].roll_dice(self.dice_values, self.remaining_rolls)

                if len(dice_to_roll) != utils.N_DICE:
                    raise utils.Penalty("Invalid dice roll")

                self.remaining_rolls -= 1
                for i in range(utils.N_DICE):
                    if dice_to_roll[i]:
                        self.dice_values[i] = random.randint(1, utils.N_FACES)

            is_yahtzee_bonus = False

            start_time = time.time()
            decision = self.agents[self.current_agent_index].choose_decision(self.dice_values)
            decision_time = time.time() - start_time

            if decision_time > 2.0:
                raise utils.Penalty("Exceeded time limit")

            if not utils.is_valid_decision(decision, self.agents[self.current_agent_index].scorecard, is_yahtzee_bonus, self.dice_values):
                raise utils.Penalty("Invalid decision")

            if is_yahtzee_bonus:
                self.agents[self.current_agent_index].scorecard['Yahtzee_Bonus'] += utils.YAHTZEE_BONUS_VALUE

            if self.current_agent_index == 0:
                self.agents[0].scorecard[decision] = utils.compute_score(self.dice_values, decision, is_yahtzee_bonus)
                self.agents[1].opponent_scorecard[decision] = self.agents[0].scorecard[decision]
            else:
                self.agents[1].scorecard[decision] = utils.compute_score(self.dice_values, decision, is_yahtzee_bonus)
                self.agents[0].opponent_scorecard[decision] = self.agents[1].scorecard[decision]

            self.current_agent_index = (self.current_agent_index + 1) % 2

    def get_winner(self):
        """Returns the winner of the game."""
        total_score1 = utils.totalScore(self.agents[0].scorecard)
        total_score2 = utils.totalScore(self.agents[1].scorecard)
        if total_score1 > total_score2:
            return self.agents[0]
        elif total_score2 > total_score1:
            return self.agents[1]
        else:
            return None

    def get_scores(self):
        """Returns the final scores of the game."""
        return [utils.totalScore(self.agents[0].scorecard), utils.totalScore(self.agents[1].scorecard)]

    def get_penalties(self):
        """Returns the penalties for the game."""
        return self.penalties
