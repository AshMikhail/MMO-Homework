from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.core.mail import send_mail



class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        pcc = ''.join(random.sample(hexdigits, 6))
        user.pcc = pcc
        user.save()
        send_mail(
            subject=f'Код Активации',
            message=f'Код для активации вашего аккаунта: {pcc}',
            from_email=None,
            recipient_list=[user.email],
        )
        return user