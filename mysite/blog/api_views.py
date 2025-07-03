from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView

from .models import Post, Comment, FavouritePost
from .serializers import PostSerializer, PostListSerializer, CommentSerializer, FavouritePostSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Lista wszystkich postów",
        description="Pobiera listę wszystkich opublikowanych postów z paginacją",
        tags=['posts'],
        responses={200: PostListSerializer(many=True)}
    )
)
class PostListAPIView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(
        summary="Szczegóły postu",
        description="Pobiera szczegółowe informacje o konkretnym poście wraz z komentarzami",
        tags=['posts'],
        responses={200: PostSerializer, 404: "Post nie został znaleziony"}
    )
)
class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(
        summary="Lista komentarzy do postu",
        description="Pobiera wszystkie aktywne komentarze dla konkretnego postu",
        tags=['comments'],
        parameters=[
            OpenApiParameter(
                name='post_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID postu'
            )
        ],
        responses={200: CommentSerializer(many=True)}
    ),
    post=extend_schema(
        summary="Dodaj komentarz do postu",
        description="Tworzy nowy komentarz dla konkretnego postu",
        tags=['comments'],
        parameters=[
            OpenApiParameter(
                name='post_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID postu'
            )
        ],
        request=CommentSerializer,
        responses={201: CommentSerializer, 400: "Błędne dane"}
    )
)
class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, active=True)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(post=post)


@extend_schema(
    summary="API Root",
    description="Główny endpoint API z listą dostępnych endpointów",
    tags=['auth'],
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
def api_root(request):
    return Response({
        'posts': request.build_absolute_uri('/blog/api/posts/'),
        'authentication': request.build_absolute_uri('/api-auth/'),
        'documentation': {
            'swagger': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'schema': request.build_absolute_uri('/api/schema/')
        }
    })


@extend_schema_view(
    get=extend_schema(
        summary="Dodaj lub usuń z ulubionych",
        description="Dodaje lub usuwa post z listy ulubionych bieżącego użytkownika",
        tags=['posts'],
        responses={ 200:{"type":"object","properties": {"favorited": {"type": "boolean"}}},
                    404:{"description": "Post nie istnieje"},
                    401:{"description": "Niezalogowany użytkownik"}
                   }
    )
)
class FavouritePostToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,post_id):
        try:
            post = Post.published.get(id=post_id)
        except Post.DoesNotExist:
            return Response({
                "detail": "Post nie istnieje"
            }, status=status.HTTP_404_NOT_FOUND)
        fav_obj,created = FavouritePost.objects.get_or_create(user=request.user,post=post)

        if not created:
            fav_obj.delete()
            return Response({"favorited": False}, status=status.HTTP_200_OK)
        return Response({"favorited": True}, status=status.HTTP_200_OK)