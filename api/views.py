from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from main.models import Bb, Comment
from .serializers import BbSerializers, BbDetailSerializers, CommentSerializers

@api_view(['GET'])
def bbs(request):
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_active=True)[:10]
        serializers = BbSerializers(bbs, many=True)
        return Response(serializers.data)

class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializers

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == 'POST':
        serializers = CommentSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, bb=pk)
        serializers = CommentSerializers(comments, many=True)
        return Response(serializers.data)

