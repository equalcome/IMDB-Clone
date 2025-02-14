from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    # StringRelatedField 關聯模型的 __str__ 方法的返回值
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    # 原本default 是 platform.ID ，把它改成platform.name
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(
        many=True, read_only=True)  # related_name='watchlist'

    class Meta:
        model = StreamPlatform
        fields = '__all__'
