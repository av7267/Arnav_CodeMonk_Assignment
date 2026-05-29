from rest_framework import serializers


class ParagraphSubmitSerializer(serializers.Serializer):
    """
    Serializer responsible for validating
    paragraph submission requests.
    """

    text = serializers.CharField(
        required=True,
        help_text=(
            "Large block of text that will be split "
            "into paragraphs and processed for indexing."
        ),
    )