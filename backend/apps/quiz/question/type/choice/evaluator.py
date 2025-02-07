from apps.quiz.question.type.base.evaluator import BaseEvaluator
from apps.quiz.question.type.choice.models import MultipleChoiceOption


class ChoiceEvaluator(BaseEvaluator):
    def compare_response_with_answer(self, question, user_value):
        print("response", question, user_value)
        choices: list[MultipleChoiceOption] = question.multiple_choice_options()
        for i in choices:
            print("choice", i)
        print("choices", choices)
