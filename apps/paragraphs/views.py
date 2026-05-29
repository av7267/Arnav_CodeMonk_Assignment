from django.db.models import Sum

from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import status

from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Paragraph, WordFrequency

from .serializers import ParagraphSubmitSerializer

from .tasks import tokenize_paragraphs

class ParagraphSubmitView(APIView):

    """

    Accepts a block of text, separates it into individual

    paragraphs, stores them in the database, and triggers

    asynchronous background processing for word analysis.

    """

    @extend_schema(

        request=ParagraphSubmitSerializer,

        responses={202: dict},

    )

    def post(self, request, *args, **kwargs):

        paragraph_serializer = ParagraphSubmitSerializer(

            data=request.data

        )

        paragraph_serializer.is_valid(

            raise_exception=True

        )

        submitted_text = (

            paragraph_serializer.validated_data["text"]

        )

        # Split paragraphs using double line breaks

        raw_paragraphs = submitted_text.split("\n\n")

        # Remove empty values and unnecessary whitespace

        cleaned_paragraphs = [

            paragraph.strip()

            for paragraph in raw_paragraphs

            if paragraph.strip()

        ]

        if not cleaned_paragraphs:

            return Response(

                {

                    "detail": (

                        "No valid paragraphs were found "

                        "in the submitted text."

                    )

                },

                status=status.HTTP_400_BAD_REQUEST,

            )

        paragraph_records = [

            Paragraph(

                user=request.user,

                content=paragraph,

            )

            for paragraph in cleaned_paragraphs

        ]

        created_paragraphs = (

            Paragraph.objects.bulk_create(

                paragraph_records

            )

        )

        created_paragraph_ids = [

            paragraph.id

            for paragraph in created_paragraphs

        ]

        # Process paragraphs asynchronously

        tokenize_paragraphs.delay(

            created_paragraph_ids,

            request.user.id,

        )

        return Response(

            {

                "detail": (

                    f"{len(created_paragraph_ids)} "

                    "paragraphs accepted for processing."

                )

            },

            status=status.HTTP_202_ACCEPTED,

        )

class ParagraphSearchView(APIView):

    """

    Searches for a word and returns the top matching

    paragraphs ranked by word frequency.

    """

    @extend_schema(

        parameters=[

            OpenApiParameter(

                name="word",

                description="Word to search for",

                required=True,

                type=str,

            )

        ],

        responses={200: dict},

    )

    def get(self, request, *args, **kwargs):

        search_word = (

            request.query_params.get("word", "")

            .lower()

            .strip()

        )

        if not search_word:

            return Response(

                {

                    "error": "Bad Request",

                    "detail": (

                        "Please provide a valid "

                        "'word' query parameter."

                    ),

                },

                status=status.HTTP_400_BAD_REQUEST,

            )

        matching_results = (

            WordFrequency.objects.filter(

                user=request.user,

                word=search_word,

            )

            .values(

                "paragraph",

                "paragraph__content",

            )

            .annotate(total=Sum("count"))

            .order_by("-total")[:10]

        )

        if not matching_results:

            return Response(

                {

                    "error": "Not Found",

                    "detail": (

                        f"The word '{search_word}' "

                        "was not found in any paragraphs."

                    ),

                },

                status=status.HTTP_404_NOT_FOUND,

            )

        formatted_results = [

            {

                "paragraph_id": str(item["paragraph"]),

                "content": item["paragraph__content"],

                "count": item["total"],

            }

            for item in matching_results

        ]

        return Response(

            {"results": formatted_results},

            status=status.HTTP_200_OK,

        )