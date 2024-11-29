# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model, including validation for future publication years."""
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure the publication year is not in the future."""
        if value > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model, with a nested list of books authored by the author."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
