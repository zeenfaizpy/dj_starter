from rest_framework import status
from rest_framework.response import Response
from rest_auth.registration.views import RegisterView as RestAuthRegisterView


class RegisterView(RestAuthRegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.is_active = False
        user.save()
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)