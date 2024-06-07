from django.views.generic import UpdateView
from django.shortcuts import render, redirect

from .models import CustomUser


class LoginWithPCC(UpdateView):
    model = CustomUser
    context_object_name = 'confirm'
    def post(self, request, *args, **kwargs):
        if 'pcc' in request.POST:
            user = CustomUser.objects.filter(pcc=request.POST['pcc'])
            if user.exists():
                user.update(is_active=True)
                user.update(pcc=None)
            else:
                return render(self.request, 'account/invalid_code.html')
            return redirect('account_login')


