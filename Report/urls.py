from django.conf.urls import patterns, include, url
from rpt.views import PrintView
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Report.views.home', name='home'),
    # url(r'^Report/', include('Report.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','rpt.views.add_student',name="add_student"),
    url(r'^st-list/$','rpt.views.student_list',name="student_list"),
    #url(r'^print-pdf/(?P<stid>.*)/$','rpt.views.student_print',name="student_print"),
    url(r'^print-pdf/(?P<stid>\d+)/$', PrintView.as_view(), name = 'print_pdf_view'),
)
