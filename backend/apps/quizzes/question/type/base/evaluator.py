class BaseEvaluatorException(Exception):
    status = 400


class BaseEvaluator:
    def get_user_submit(self):
        raise Exception('Not implemented')

    def apply(self, question, user_value):
        raise Exception('Not implemented')

    def compare_response_with_answer(self, question, user_value):
        raise Exception('Not implemented')
