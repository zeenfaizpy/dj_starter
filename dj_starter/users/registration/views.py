from rest_framework import status
from rest_framework.response import Response
from rest_auth.registration.views import RegisterView as RestAuthRegisterView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

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


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get(self, request, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        self.change_user_active(confirmation)
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
    
    def change_user_active(self, confirmation):
        user = confirmation.email_address.user
        user.is_active = True
        user.save()

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return Response({'detail': 'Failure'}, 
                                status=status.HTTP_404_NOT_FOUND)
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs