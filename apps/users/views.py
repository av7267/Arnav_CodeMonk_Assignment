from drf_spectacular.utils import extend_schema

from rest_framework import generics, status

from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):

    """

    Handles registration for new users.

    Validates the incoming request data and creates

    a new user account with a securely hashed password.

    """

    permission_classes = (AllowAny,)

    serializer_class = RegisterSerializer

    @extend_schema(responses={201: UserSerializer})

    def post(self, request, *args, **kwargs):

        registration_serializer = self.get_serializer(

            data=request.data

        )

        registration_serializer.is_valid(

            raise_exception=True

        )

        created_user = registration_serializer.save()

        return Response(

            UserSerializer(created_user).data,

            status=status.HTTP_201_CREATED,

        )