import json
from db import getConnection
from exceptions.customException import NoQuestionFoundException, NoAnswerFoundException


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
    query = "SELECT id, correct_option  FROM match_questions WHERE match_id = %s"
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

# def updateRewards(matchId, userId, 

def compareAndUpdateRewards(matchId, bets, matchQuestions):
    for bet in bets:
        userBet = json.loads(bet["answers"])
        # print(userBet)
        # exit()
        for question in matchQuestions:

            if question["correct_option"] == userBet[str(question["id"])]["option"]:
                print("user won the bet")
            else:
                print("user lost the bet")


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

        compareAndUpdateRewards(
            matchId=match["id"], bets=bets, matchQuestions=matchQuestions
        )


except Exception as e:
    print(e)
