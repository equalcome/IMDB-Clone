from django.shortcuts import get_object_or_404
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

from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api import serializers, pagination
from watchlist_app.api.throttling import ReviewCreateTrottle, ReviewListTrottle


class UserReview(generics.ListAPIView):
    # permission_classes = [IsAuthenticated] #頁面進入許可，要有驗證才能
    # throttle_classes = [ReviewListTrottle]
    # throttle_scope = 'review-detail'

    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)  #User 模型有一個 username 欄位     #review_user 是指向 User 模型的外來鍵

    def get_queryset(self):
        username = self.request.query_params.get(
            'username', None)  # 會取得 URL 查詢參數
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):  # POST  #serializer.is_valid()
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateTrottle]  # 限制流量的東東

    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)  # 加載了一個 WatchList 實例

        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watch!!!!")

        if watchlist.number_rating == 0:  # 第一個評論的
            # 執行了 serializer.is_valid() 後，validated_data 才會被填充
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data['rating'])/2  # 應該不是除以2吧? 要平均

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()  # 將當前 WatchList 模型實例的變更(avg_rating 和 number_rating)保存到DB中

        # 它會自動處理來自 request.data（用戶提供的輸入）的字段，但對於未提供的字段（如 watchlist 和 review_user），需要在調用 save() 時手動傳遞。
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):  # GET
    # permission_classes = [IsAuthenticated] #頁面進入許可，要有驗證才能
    throttle_classes = [ReviewListTrottle]
    throttle_scope = 'review-detail'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)  # pk=id幾號電影的所有評論


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):  # GET PUT/PATCH DELETE
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
