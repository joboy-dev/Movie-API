# from rest_framework import mixins
# from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import (WatchListSerializer, StreamPlatformSerializer, 
                            ReviewSerializer)
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from .pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination

# class based view

# filter reviews for a particular user
class UserReview(generics.ListAPIView):

    # we have to overwrite the queryset to prevent us from getting all reviews
    serializer_class = ReviewSerializer

    # custom throttle classes
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle] 

    # filtering based on user (easy way)
    # overwriting the queryset

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     # we filter based on the user review we are looking ofr
    #     return Review.objects.filter(review_user__username=username)  # get review_user and jump on to username by using __username to match it. You only do this when it is a foreign key
        # __username - username here represents a field in the model being related to through review_user. In this case the model is User and it has a field called username there
    
    # filtering based on query parameter
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)

#  GenericAPIViews and queryset method overwriting
class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    # custom throttle classes
    throttle_classes = [ReviewCreateThrottle]
    

    def get_queryset(self):
        return Review.objects.all()

    # overwrite our create method
    def perform_create(self, serializer):
        id = self.kwargs.get('pk') # normally this would be part of the function definition but not in this case so we have to retrieve it this way
        
        # since we want to add review to a particular watchlist, we have to retrieve that watchlist
        movie = WatchList.objects.get(pk=id)

        # store the request of the current user
        current_user = self.request.user

        # check if a review already exists for the current user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=current_user)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this watchlist')
        
        # calculation for average rating
        if movie.number_of_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating']  # note that when working with serializer data, ensure you get validated data from serializer because data from models may not be valid
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
        
        movie.number_of_ratings = movie.number_of_ratings + 1
        movie.save()

        serializer.save(watchlist=movie, review_user=current_user)
        

class ReviewList(generics.ListAPIView):

    # we have to overwrite the queryset to prevent us from getting all reviews
    serializer_class = ReviewSerializer

    # rest framework permission classes
    # permission_classes = [IsAuthenticated]

    # rest framework throttle classes
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]

    # custom throttle classes
    throttle_classes = [ReviewListThrottle, AnonRateThrottle] 

    # filtering with django_filter
    filter_backends = [DjangoFilterBackend]
    # selecting the fields to filter
    filterset_fields = ['review_user__username', 'active']

    # overwriting the queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        # we filter based on the movie reviews we are looking for
        return Review.objects.filter(watchlist=pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):

    # custom permission classes
    permission_classes = [ReviewUserOrReadOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # scoped rate throttle
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'



# ModelViewSet and ReadOnlyModelViewSet
class StreamPlatformVS(viewsets.ModelViewSet):

    permission_classes = [AdminOrReadOnly]

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer

class WatchListGV(generics.ListAPIView):

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle] 

    # generic fitering
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # search options (SearchFilter)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']

    # OrderingFilter
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['title', 'platform__name']

    pagination_class = WatchListCPagination
    # note that when using CursorPagination, do not have any OrderingFilter backend in use since it has its own ordering filter


class WatchListAV(APIView):

    permission_classes = [AdminOrReadOnly]

    def get(self, request):
        # get all items
        movies = WatchList.objects.all()
        # store the items
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
        

    def post(self, request):
        # store all data entered by the user. request.data holds all that data
        serializer = WatchListSerializer(data=request.data)

        # check if serializer is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class WatchDetailsAV(APIView):

    permission_classes = [AdminOrReadOnly]

    def get(self, request, pk):
        # check if the object being requested for  is in the database
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        # store rretieved item
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)


    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk) 
        serializer = WatchListSerializer(movie, data=request.data)  

        # check if serializer is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk) 
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 





# class StreamPlatformAV(APIView):

#     def get(self, request):
#         streamPlatforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(streamPlatforms, many=True)
#         return Response(serializer.data)

    
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



# class StreamPlatformDetailAV(APIView):

#     def get(delf, request, pk):
#         try:
#             streamPlatform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StreamPlatformSerializer(streamPlatform, context={'request':request})
#         return Response(serializer.data)


#     def put(self, request, pk):
#         streamPlatform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(streamPlatform, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


#     def delete(self, request, pk):
#         streamPlatform = StreamPlatform.objects.get(pk=pk)
#         streamPlatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# viewset
# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def update(self, request, pk):
#         queryset = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(queryset, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def destroy(self, request, pk):
#         queryset = StreamPlatform.objects.get(pk=pk)
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)






# GenericAPIView and Mixins
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetails(
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     generics.GenericAPIView
# ):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         try:
#             return self.retrieve(request, *args, **kwargs)
#         except Review.DoesNotExist:
#             return Response({'Error':'Review not found'}, status=status.HTTP_404_NOT_FOUND)







# function based view
# # movie list
# @api_view(['GET', 'POST'])  # decorator. By default it is a get request
# def movie_list(request):
#     # GET request
#     if request.method == 'GET':
#         movies = WatchList.objects.all()
#         # using the serializer
#         serializer = WatchListSerializer(movies, many=True)  # many=True is needed since we are getting more than one field in the object
#         return Response(serializer.data)
    
#     # POST request
#     if request.method == 'POST':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# # individual movie
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     # get individual movie
#     if request.method == 'GET':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#             # serializer = WatchListSerializer(movie)
#             # return Response(serializer.data)
#         except WatchList.DoesNotExist:
#             return Response({'Error': 'WatchList Not Found'}, status=status.HTTP_404_NOT_FOUND)  # sending response in form of dictionary response

#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
    
#     # update movie details
#     if request.method == 'PUT':
#         movie = WatchList.objects.get(pk=pk)  # it is necessry to get the specific item we want to update
#         serializer = WatchListSerializer(movie, data=request.data)  # fetching data put in previously by the user
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # delete movie
#     if request.method == 'DELETE':
#         movie = WatchList.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)  # since we deleted, we send a status code of 204
