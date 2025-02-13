from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import ReviewList, ReviewDetail, ReviewCreate, WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV, StreamPlatformVS, UserReview, WatchListGV


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watchlist-list'), 
    path('<int:pk>/', WatchDetailAV.as_view(), name='watchlist-detail'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),
    
    path('', include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name='streamplatform-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),    #創建一個與特定 WatchList 關聯的 Review
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),    #列出與某個 WatchList 關聯的所有 Review
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),  #操作單個 Review 對象（查看、更新或刪除）
    
    path('reviews/', UserReview.as_view(), name='user-review-detail'),  #該user的所留的reviews
    

]

 