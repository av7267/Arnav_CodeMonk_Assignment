import re
from collections import Counter
from celery import shared_task
from .models import Paragraph, WordFrequency
@shared_task


def tokenize_paragraphs(paragraph_ids, user_id):
    """
    Background task responsible for processing paragraphs
    and storing word frequency statistics.
    Running this asynchronously prevents large text-processing
    operations from slowing down API responses.
    """
    for paragraph_id in paragraph_ids:
        try:
            paragraph = Paragraph.objects.get(
                id=paragraph_id
            )
        except Paragraph.DoesNotExist:
            continue
        # Extract words while ignoring punctuation
        normalized_words = re.findall(
            r"[a-zA-Z0-9']+",
            paragraph.content.lower(),
        )
        # Count occurrences of each word
        word_frequency_map = Counter(
            normalized_words
        )
        frequency_records = [
            WordFrequency(
                user_id=user_id,
                paragraph=paragraph,
                word=word,
                count=frequency,
            )
            for word, frequency in word_frequency_map.items()
        ]
        # Insert all frequency records efficiently
        WordFrequency.objects.bulk_create(
            frequency_records,
            ignore_conflicts=True,

        )