from django.conf.urls.defaults import *

urlpatterns = patterns('shipping.views',
    (r'^\/?$', 'index'),
    (r'^\/pushes\/?$', 'pushes'),
    (r'^\/dashboard\/?$', 'dashboard'),
    (r'^\/l10n-changesets$', 'l10n_changesets'),
    (r'^\/shipped-locales$', 'shipped_locales'),
    (r'^\/api\/pushes$', 'pushes_json'),
    (r'^\/api\/signoffs$', 'signoff_json'),
    (r'^\/diff$', 'diff_app'),
    (r'^\/milestones$', 'milestones'),
    (r'^\/stones-data$', 'stones_data'),
    (r'^\/open-mstone$', 'open_mstone'),
    (r'^\/clear-mstone$', 'clear_mstone'),
    (r'^\/confirm-ship$', 'confirm_ship_mstone'),
    (r'^\/confirm-drill$', 'confirm_drill_mstone'),
    (r'^\/drill$', 'drill_mstone'),
    (r'^\/ship$', 'ship_mstone'),
)

urlpatterns += patterns('shipping.views.milestone',
    (r'^\/about-milestone/(.*)', 'about'),
    (r'^\/milestone-stati/(.*)', 'stati'),
)
