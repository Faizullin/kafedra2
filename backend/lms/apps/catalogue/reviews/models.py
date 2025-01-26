from lms.apps.catalogue.reviews.abstract_models import (
    AbstractProductReview,
    AbstractVote,
)
from lms.core.loading import is_model_registered

if not is_model_registered("reviews", "ProductReview"):

    class ProductReview(AbstractProductReview):
        pass


if not is_model_registered("reviews", "Vote"):

    class Vote(AbstractVote):
        pass
