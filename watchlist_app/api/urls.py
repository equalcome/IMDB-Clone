from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # using API view
    path('', views.WatchListAV.as_view(), name='watchlist-list'),  # 全部電影清單
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='watchlist-detail'),

    # using view sets and router.
    path('', include(router.urls)),

    # generic views
    path('<int:pk>/reviews/create/', views.ReviewCreate.as_view(),
         name='review-create'),  # 創建一個與特定 WatchList 關聯的 Review
    path('<int:pk>/reviews/', views.ReviewList.as_view(),
         name='review-list'),  # 列出與某個 WatchList 關聯的所有 Review
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(),
         name='review-detail'),  # 操作單個 Review 對象（查看、更新或刪除）

    # custom made
    path('user-reviews/', views.UserReview.as_view(),
         name='user-review-detail'),  # 該user的所留的reviews


]
