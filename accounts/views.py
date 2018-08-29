# 클래스 기반의 Rest CRUD 처리
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.serializers import *
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist

from accounts.permissions import IsAuthenticatedOrCreate
from django.contrib.auth.models import User

# generics 에 목록과 생성 API 가 정의되어 있다
class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# generics 에 상세, 수정, 삭제 API가 정의되어 있다
class UserDetail(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UserDetailEdit(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticatedOrCreate,)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    # def update(self, request, pk=, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object(pk=pk)
    # #    instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        Profile = self.get_object(pk)
        serializer = ProfileSerializer(Profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuskerList(viewsets.ModelViewSet):
    queryset = Busker.objects.all()
    serializer_class = BuskerSerializer

class ConnectionList(viewsets.ModelViewSet):
    queryset = Connections.objects.all()
    serializer_class = ConnectionsSerializer

class ConnectionsView(generics.CreateAPIView):
    queryset = Connections.objects.all()
    serializer_class = ConnectionsSerializer

    def get_object(self, pk):
        try:
            return Connections.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = ConnectionsSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = ConnectionsSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#이미지 전송을 위해 json형식이 아닌 formparser로 데이터 전송
class BuskerView(generics.CreateAPIView):
    queryset = Busker.objects.all()
    serializer_class = BuskerSerializer
    parser_classes = (MultiPartParser,)

    #busker_id로 버스커 객체 얻어옴
    def get_object(self, pk):
        try:
            return Busker.objects.get(pk=pk)
        except Busker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = BuskerSerializer(event)
        return Response(serializer.data)

    #버스커 객체 생성
    def post(self, request, *args, **kwargs):
        serializer_class = BuskerSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    #버스커 객체 삭제
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#회원가입 뷰 권한 처리를 위해 permission
class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

#토큰 받아오는 뷰
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({'token': token.key, 'id': token.user_id, 'username': user.username, 'email': user.email,
                         'user_phone': user.profile.user_phone
                         })
