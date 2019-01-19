from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class XYUserRequiredMixin(object):

    @method_decorator(user_passes_test(
        lambda u: hasattr(u, 'boss'),
        login_url="account:login")
    )
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        print(user, 1)
        return super(XYUserRequiredMixin, self).dispatch(request, *args, **kwargs)