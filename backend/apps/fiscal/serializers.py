"""Serializers for this domain."""
from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
