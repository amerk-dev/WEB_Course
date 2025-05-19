from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Watch, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class WatchSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)  # для загрузки base64
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_image(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("File size too big! Max 5MB")
        if not value.content_type in ['image/jpeg', 'image/png']:
            raise serializers.ValidationError("Only JPEG/PNG allowed")
        return value

    class Meta:
        model = Watch
        fields = [
            'id',
            'name',
            'brand',
            'brand_id',
            'description',
            'price',
            'watch_type',
            'image',
            'in_stock',
            'created_at'
        ]
        read_only_fields = ['created_at']