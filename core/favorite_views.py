from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import permissions
from .models import FavoriteStock
from .serializers import FavoriteStockSerializer


class FavoriteStockListView(ListAPIView):
    serializer_class = FavoriteStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteStock.objects.filter(user=self.request.user).order_by("-added_on")  # Order by added_on descending


class FavoriteStockCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteStockSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteStockDeleteView(DestroyAPIView):
    serializer_class = FavoriteStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteStock.objects.filter(user=self.request.user)
