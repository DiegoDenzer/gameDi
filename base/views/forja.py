from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class CriarItem(View, LoginRequiredMixin):
    login_url = '/'

    def get(self, request):
        pass
