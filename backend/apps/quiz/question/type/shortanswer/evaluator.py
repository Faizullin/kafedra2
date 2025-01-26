import re

from apps.assignments.question.type.base.evaluator import BaseEvaluator


class ShortAnswerEvaluator(BaseEvaluator):
    def apply(self, question, user_value):
        correct_answers = question.short_answer_option.correct_answers
        if self.question.short_answer_option.use_case:
            return user_answer in correct_answers
        return user_answer.lower() in [answer.lower() for answer in correct_answers]

    def compare_response_with_answer(self, response, question_answer, question):
        answer = response.get("answer", None)
        if (answer["answer"] is None) or not (response['answer']):
            return False
        return self.compare_string_with_wildcard(response['answer'], answer.answer, not question.use_case)

    def compare_string_with_wildcard(self, string, pattern, ignore_case):
        bits = re.split(r'(?<!\\)\*+/', pattern)
        escapedbits = [re.escape(bit.replace('\\*', '*')) for bit in bits]
        regexp = r'^' + r'.*'.join(escapedbits) + r'$'

        if ignore_case:
            regexp += 'i'

        return re.match(regexp, string.strip()) is not None

    def grade(self, response, question):
        answers = self.get_answers(question)
        for answer in answers:
            if self.compare_response_with_answer(response, answer, question):
                return answer
        return None

    def grade_response(self, response, question):
        answer = self.grade(response, question)
        if answer:
            return answer.fraction, get_state(answer.fraction)

        return 0, state_wrong
