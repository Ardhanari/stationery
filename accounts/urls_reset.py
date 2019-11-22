from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_confirm, password_reset_done

urlpatterns = [
    url('^$', password_reset, {'post_reset_redirect': reverse_lazy('password_reset_done')}, name='password_reset'),
    url(r'^done/$', password_reset_done, name='password_reset_done'),
    url(r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('password_reset_complete')}, name='password_reset_confirm'),
    url('^complete/$', password_reset_complete, name='password_reset_complete')
]

# consider adding custom templates for email? 
# url('^password_reset/$', auth_views.password_reset,
#         {
#             'template_name': 'accounts/reset_password.html',
#             'email_template_name': 'email/password_reset/password_reset.txt',
#             'html_email_template_name': 'email/password_reset/password_reset.html',
#             'subject_template_name': 'email/password_reset/password_reset_subject.txt'
#         },
#         name='password_reset'),