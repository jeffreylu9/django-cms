# Thanks to the tutorial here: http://www.tryolabs.com/Blog/2012/06/18/django-administration-interface-non-staff-users/
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserAdminAuthenticationForm(AuthenticationForm):
    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput,
                                initial=1,
                                error_messages={'required': ugettext_lazy(
                                "Please log in again, because your session has"
                                " expired.")})
 
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = "This is an error message, yo"
         
        if username and password:
            self.user_cache = authenticate(username=username,
            password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your "
                                        "username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            # Removed check for is_staff here!
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data
    
class CMSAdmin(AdminSite):
    
    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active
 
cmsadmin = CMSAdmin(name='cmsadmin')
# Run cmsadmin.register() for each model we wish to register
# for our admin interface for users
 
# Run admin.site.register() for each model we wish to register
# with the REAL django admin!

