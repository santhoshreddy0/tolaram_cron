from models.db import getConnection
from exceptions.customException import *
import json


class matchBets:
    listIdColumn = "round_id"
    betsTable = "round_bets"
    listTable = "rounds"
    questionsTable = "round_questions"
    limit = 1

    def __init__(self):
        self.conn = getConnection()

    def _getMatches(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"SELECT id FROM {self.listTable} WHERE bet_status = 'process' AND can_bet = '0'",
            )
            matches = cursor.fetchall()
            return matches
        except Exception as e:
            print(e)
            raise Exception("Error in getMatches")

    def _getQuestions(self, id):
        cursor = self.conn.cursor()
        query = f"SELECT id, correct_option, options  FROM {self.questionsTable} WHERE {self.listIdColumn} = {id}"
        cursor.execute(query)
        questions = cursor.fetchall()

        if not questions:
            raise NoQuestionFoundException(
                "No questions found for match id: " + str(id)
            )

        for question in questions:
            if question["correct_option"] == None:
                raise NoAnswerFoundException(
                    "No correct option found for question id: " + str(question["id"])
                )

        return questions

    def _getBets(self, id, limit, offset):
        cursor = self.conn.cursor()
        query = f"SELECT id, user_id, answers FROM {self.betsTable} WHERE {self.listIdColumn} = {id} limit {limit} offset {offset}"
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

                totalPoints += points
            self._updateRewards(bet["id"], points=totalPoints)

    def _updateListRowStatus(self, matchId):

        cursor = self.conn.cursor()
        query = (
            f"UPDATE {self.listTable} SET bet_status = 'completed' WHERE id = {matchId}"
        )
        cursor.execute(query)

    def _getTotalBets(self, matchId):
        cursor = self.conn.cursor()
        query = f"SELECT COUNT(id) as total_bets FROM {self.betsTable} WHERE {self.listIdColumn} = {matchId}"
        cursor.execute(query)
        totalBets = cursor.fetchone()

        return totalBets["total_bets"]

    def process(self):
        try:

            matches = self._getMatches()
            print(matches)
            if matches == None or len(matches) == 0:
                raise NoMatchFoundException("No matches found")
            for match in matches:
                print("round --> ", match["id"])

                try:
                    questions = self._getQuestions(id=match["id"])
                except NoQuestionFoundException as e:
                    print(e)
                    continue
                except NoAnswerFoundException as e:
                    print(e)
                    continue
                totalBets = self._getTotalBets(match["id"])

                for i in range(0, totalBets, self.limit):
                    bets = self._getBets(
                        id=match["id"],
                        limit=self.limit,
                        offset=i,
                    )

                    self._compareAndUpdateRewards(bets=bets, questions=questions)
                self._updateListRowStatus(matchId=match['id'])

                print("Rounds completed successfully")

        except Exception as e:
            print(e)


def main():
    bets = matchBets()
    bets.process()


if __name__ == "__main__":
    main()
