from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import *
from myapp.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.permissions import AllowAny,IsAuthenticated

# Registration
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'OK',
                'message': 'User created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        serializer = CustomUserSerializer(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data,  
        })
    
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# user edit,delete,detail

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({'status': 'Not Found', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response({'status': 'OK', 'message': 'User details', 'data': serializer.data})
    
    elif request.method == 'PUT':
        
        mutable_data = request.data.copy()
        
       
        if 'password' in mutable_data:
            mutable_data['password'] = make_password(mutable_data['password'])

        serializer = CustomUserSerializer(user, data=mutable_data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'OK', 'message': 'User updated successfully', 'data': serializer.data})
        return Response({
            'status': 'Bad Request',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response({'status': 'OK', 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
# list users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({
            'status': 'OK',
            'message': 'List of users',
            'data': serializer.data
        })