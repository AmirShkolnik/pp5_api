from rest_framework import serializers
from .models import Course, Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'course', 'content',
            'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        if data['rating'] < 1 or data['rating'] > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        if data.get('rating', 0) < 1 or data.get('rating', 0) > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return data


class CourseSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'excerpt', 'description', 'course_type',
            'image', 'price', 'price_display', 'reviews', 'average_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['average_rating', 'reviews']
        extra_kwargs = {
            'title': {'error_messages': {'blank': 'Title is required.'}},
            'excerpt': {'error_messages': {'blank': 'Excerpt is required.'}},
            'description': {'error_messages': {'blank':
                            'Description is required.'}},
            'course_type': {'error_messages': {'blank':
                            'Course type is required.'}},
            'image': {'error_messages': {'blank': 'Image is required.'}},
            'price': {'error_messages': {'blank': 'Price is required.'}},
        }

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_price_display(self, obj):
        return f"{obj.price} $"
