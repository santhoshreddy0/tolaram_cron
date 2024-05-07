class NoAnswerFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoQuestionFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        