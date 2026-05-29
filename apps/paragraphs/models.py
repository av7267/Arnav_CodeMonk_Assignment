from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db import models



User = get_user_model()
class Paragraph(models.Model):
    """
    Stores paragraphs submitted by users for
    asynchronous text processing and analysis.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return (
            f"Paragraph {self.id} "
            f"submitted by {self.user.email}"
        )
    

class WordFrequency(models.Model):
    """
    Stores word occurrence counts for each paragraph.
    Used to support fast keyword searching and analytics.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    word = models.CharField(max_length=100, db_index=True)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "paragraph", "word")
        indexes = [models.Index(fields=["user", "word"])]

    def __str__(self):
        return (
            f"'{self.word}' appears "
            f"{self.count} times in "
            f"Paragraph {self.paragraph.id}"
        )