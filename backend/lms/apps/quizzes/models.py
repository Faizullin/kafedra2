from .abstract_models import (
    AbstractLMSAssessment,
    AbstractLMSQuestionGroup,
    AbstractLMSQuiz,
    AbstractLMSQuizQuestion,
    AbstractLMSQuestionAnswer,
    AbstractLMSQuizResult,
    AbstractLMSQuizSubmission,
)


class LMSAssessment(AbstractLMSAssessment):
    pass


class LMSQuestionGroup(AbstractLMSQuestionGroup):
    pass


class LMSQuiz(AbstractLMSQuiz):
    pass


class LMSQuizQuestion(AbstractLMSQuizQuestion):
    pass


class LMSQuestionAnswer(AbstractLMSQuestionAnswer):
    pass


class LMSQuizResult(AbstractLMSQuizResult):
    pass


class LMSQuizSubmission(AbstractLMSQuizSubmission):
    pass
