from django.urls import path

from .views import (
    ParagraphSearchView,
    ParagraphSubmitView,
)

urlpatterns = [
    # Submit paragraphs for processing
    path(
        "",
        ParagraphSubmitView.as_view(),
        name="paragraph-submit",
    ),

    # Search paragraphs by word frequency
    path(
        "search/",
        ParagraphSearchView.as_view(),
        name="paragraph-search",
    ),
]