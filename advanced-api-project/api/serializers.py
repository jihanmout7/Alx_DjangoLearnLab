from rest_framework import serializers
from .models import Author, Book
import datetime  # Make sure to import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # You can list the fields explicitly if needed

    def validate_publication_year(self, value):
        # Check if the publication year is in the future
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer for related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('name', 'books')