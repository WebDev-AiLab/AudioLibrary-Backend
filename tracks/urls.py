from django.urls import path, include
from .views import TrackView, PlayView, StylesListing, ArtistView, LikeView, LabelView, CommentView, SubmissionView, RatingListing, CommentArtistView

urlpatterns = [
    # tracks/track
    path('', TrackView.as_view({'get': 'list', 'post': 'create'})),
    path('<uuid:pk>/', TrackView.as_view({'get': 'retrieve'})),
    path('slug/<str:slug>/', TrackView.as_view({'get': 'retrieve_slug'})),

    # interactions (todo move to interactions)
    path('<uuid:pk>/plays/', PlayView.as_view()),
    path('<uuid:pk>/likes/', LikeView.as_view()),
    path('<uuid:pk>/comments/', CommentView.as_view({'get': 'list', 'post': 'post'})),
    path('<uuid:pk>/comments/<uuid:comment_pk>/', CommentView.as_view({'delete': 'delete'})),

    path('artists/<uuid:pk>/comments/', CommentArtistView.as_view({'get': 'list', 'post': 'post'})),
    path('artists/<uuid:pk>/comments/<uuid:comment_pk>/', CommentArtistView.as_view({'delete': 'delete'})),

    # artists
    path('artists/', ArtistView.as_view({'get': 'list', 'post': 'create'})),
    path('artists/<str:slug>/', ArtistView.as_view({'get': 'retrieve'})),

    # labels
    path('labels/', LabelView.as_view({'get': 'list'})),
    path('labels/<str:slug>/', LabelView.as_view({'get': 'retrieve'})),

    # styles
    path('styles/', StylesListing.as_view()),

    # ratings
    path('ratings/', RatingListing.as_view()),

    # submit
    path('submit/', SubmissionView.as_view()),

    # ajax shit
    path('ajax/styles/', StylesListing.as_view())
]