import json
from models.db import getConnection
from exceptions.customException import NoQuestionFoundException, NoAnswerFoundException
from matchBets import matchBets


def getMatches():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM matches WHERE bet_status = 'process'")
        matches = cursor.fetchall()
        return matches
    except Exception as e:
        print(e)
        raise Exception("Error in getMatches")


def getMatchQuestions(matchId):
    conn = getConnection()
    cursor = conn.cursor()
    query = (
        "SELECT id, correct_option, options  FROM match_questions WHERE match_id = %s"
    )
    cursor.execute(query, (matchId,))
    questions = cursor.fetchall()

    if not questions:
        raise NoQuestionFoundException(
            "No questions found for match id: " + str(match["id"])
        )

    for question in questions:
        if question["correct_option"] == None:
            raise NoAnswerFoundException(
                "No correct option found for question id: " + str(question["id"])
            )

    return questions


def getMatchBets(matchId):
    conn = getConnection()
    cursor = conn.cursor()
    query = "SELECT id, user_id, answers FROM match_bets WHERE match_id = %s"
    cursor.execute(query, (matchId,))
    bets = cursor.fetchall()
    return bets


def updateRewards(betId, points):
    conn = getConnection()
    cursor = conn.cursor()
    query = "UPDATE match_bets SET points = %s, can_show_points = '1' WHERE id = %s"
    cursor.execute(query, (points, betId))


def compareAndUpdateRewards(bets, matchQuestions):
    for bet in bets:
        userBet = json.loads(bet["answers"])

        for question in matchQuestions:
            options = json.loads(question["options"])

            if question["correct_option"] == userBet[str(question["id"])]["option"]:
                chosenOptionDetails = [
                    option
                    for option in options
                    if str(option["id"]) == question["correct_option"]
                ]
                odds = float(chosenOptionDetails[0]["odds"])
                amount = float(userBet[str(question["id"])]["amount"])
                points = odds * amount
                updateRewards(bet["id"], points=points)
            else:
                updateRewards(bet["id"], 0)


def updateMatchStatus(matchId):
    conn = getConnection()
    cursor = conn.cursor()
    query = "UPDATE matches SET bet_status = 'completed' WHERE id = %s"
    cursor.execute(query, (matchId,))


def start():
    try:
        matches = getMatches()
        for match in matches:
            print("match --> ", match["id"])
            try:
                matchQuestions = getMatchQuestions(matchId=match["id"])
            except NoQuestionFoundException as e:
                print(e)
                continue
            except NoAnswerFoundException as e:
                print(e)
                continue

            bets = getMatchBets(
                matchId=match["id"],
            )

            compareAndUpdateRewards(bets=bets, matchQuestions=matchQuestions)
            updateMatchStatus(match["id"])
            print("Match completed successfully")

    except Exception as e:
        print(e)


def main():
    bets = matchBets()
    bets.process()


if __name__ == "__main__":
    main()
