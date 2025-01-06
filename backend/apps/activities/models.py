from utils.models import models, AbstractTimestampedModel


class ActivityLog(AbstractTimestampedModel):
    message = models.TextField()

    def __str__(self):
        return f"[{self.created_at}]{self.message}"
