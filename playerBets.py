from models.db import getConnection
from exceptions.customException import *
import json


class matchBets:
    betsTable = "best_player_bets"
    questionsTable = "best_player_questions"
    limit = 1

    def __init__(self):
        self.conn = getConnection()

    def _getQuestions(self):
        cursor = self.conn.cursor()
        query = f"SELECT id, correct_option, options  FROM {self.questionsTable}"
        cursor.execute(query)
        questions = cursor.fetchall()

        if not questions:
            raise NoQuestionFoundException("No questions found for match id: ")

        for question in questions:
            if question["correct_option"] == None:
                raise NoAnswerFoundException(
                    "No correct option found for question id: " + str(question["id"])
                )

        return questions

    def _getBets(self, limit, offset):
        cursor = self.conn.cursor()
        query = f"SELECT id, user_id, answers FROM {self.betsTable} limit {limit} offset {offset}"
        cursor.execute(query)
        bets = cursor.fetchall()
        return bets

    def _updateRewards(self, betId, points):

        cursor = self.conn.cursor()
        query = f"UPDATE {self.betsTable} SET points = {points}, can_show_points = '1' WHERE id = {betId}"
        cursor.execute(query)

    def _compareAndUpdateRewards(self, bets, questions):
        for bet in bets:
            userBet = json.loads(bet["answers"])

            totalPoints = 0
            for question in questions:
                options = json.loads(question["options"])

                if str(question["correct_option"]) == str(userBet[str(question["id"])]["option"]):
                    chosenOptionDetails = [
                        option
                        for option in options
                        if str(option["id"]) == question["correct_option"]
                    ]
                    odds = float(chosenOptionDetails[0]["odds"])
                    amount = float(userBet[str(question["id"])]["amount"])
                    points = odds * amount - amount
                else:
                    points = -1 * float(userBet[str(question["id"])]["amount"])

                totalPoints += points
            self._updateRewards(bet["id"], points=totalPoints)

    def _getTotalBets(self):
        cursor = self.conn.cursor()
        query = f"SELECT COUNT(id) as total_bets FROM {self.betsTable} "
        cursor.execute(query)
        totalBets = cursor.fetchone()

        return totalBets["total_bets"]

    def process(self):
        try:

            try:
                questions = self._getQuestions()
            except NoQuestionFoundException as e:
                print(e)

            except NoAnswerFoundException as e:
                print(e)

            totalBets = self._getTotalBets()
            

            for i in range(0, totalBets, self.limit):
                bets = self._getBets(
                    limit=self.limit,
                    offset=i,
                )

                self._compareAndUpdateRewards(bets=bets, questions=questions)

            print("Player bets completed successfully")

        except Exception as e:
            print(e)


def main():
    bets = matchBets()
    bets.process()


if __name__ == "__main__":
    main()
