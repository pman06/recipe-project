from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

    def validate_name(self, name):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        exists = Tag.objects.filter(user=user, name=name).exists()
        if(exists):
            raise serializers.ValidationError("Duplicate submission!")
        return name


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class UserTagField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Tag.objects.filter(user=user)
        return queryset


class RecipeSerializer(serializers.ModelSerializer):
    """Serielizer for recipe objects"""
    # request = context.get('request')
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = UserTagField(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'tags', 'time_minutes',
                  'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
