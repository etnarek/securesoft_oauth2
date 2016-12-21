from registration.backends.simple.views import RegistrationView

class CustomRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return self.get_form_kwargs()['data'].get('next')
