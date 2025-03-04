namespace = "dashboard"

url_reverses_dict = {
    "quiz-quiz-list": "dashboard/quiz/quiz",
    "quiz-quiz-list-api": "api/v1/dashboard/quiz/quiz",
    "quiz-quiz-create": "dashboard/quiz/quiz/add",
    "quiz-quiz-update": "dashboard/quiz/quiz/<int:pk>/edit",
    "quiz-quiz-delete": "dashboard/quiz/quiz/<int:pk>/delete",
    "quiz-question-group-list": "dashboard/quiz/questions/groups",
    "quiz-question-group-list-api": "api/v1/dashboard/quiz/questions/groups",
    "quiz-question-group-create": "dashboard/quiz/questions/groups/add",
    "quiz-question-group-update": "dashboard/quiz/questions/groups/<int:pk>/edit",
    "quiz-question-group-delete": "dashboard/quiz/questions/groups/<int:pk>/delete",
    "quiz-question-list": "dashboard/quiz/questions",
    "quiz-question-list-api": "api/v1/dashboard/questions",
    "quiz-question-create": "dashboard/quiz/questions/add",
    "quiz-question-update": "dashboard/quiz/questions/<int:pk>/edit",
    "quiz-question-delete": "dashboard/quiz/questions/<int:pk>/delete",
    "quiz-question-qtype-detail": "dashboard/quiz/questions/qtype",
    "quiz-question-create-api": "api/v1/dashboard/quiz/questions",
    "quiz-question-update-api": "api/v1/dashboard/quiz/questions/<int:pk>/edit",
}
