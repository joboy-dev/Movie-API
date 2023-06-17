from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (WatchListAV, WatchListGV, WatchDetailsAV, StreamPlatformVS, ReviewList, ReviewDetails,
                    ReviewCreate, UserReview)

# StreamPlatformDetailAV
# StreamPlatformAV

app_name = 'watchlist_app'

# router
router = DefaultRouter()  # register route. only use it for simple stuff

# for list, the default will be basename-list(streamplatform-list)
# for detail, the default will be basename-detail(streamplatform-detail)
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # path('list/', WatchListAV.as_view(), name='movie-list'),
    path('list/', WatchListGV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailsAV.as_view(), name='movie-detail'),

    path('', include(router.urls)),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    # access all reviews for one movie
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    # access a psecific review for one movie
    path('review/<int:pk>/', ReviewDetails.as_view(), name='review-detail'),
    
    #  access reviews of a particular user
    # path('reviews/<str:username>/', UserReview.as_view(), name='user-review'),
    path('reviews/', UserReview.as_view(), name='user-review'),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetails.as_view(), name='review-detail'),
]
