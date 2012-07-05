# -*- coding: utf-8 -*-


def login( request ):
  from django.contrib import auth
  if u'Shibboleth-eppn' in request.META and request.META[ u'Shibboleth-eppn' ] in settings_app.PERMITTED_ADMINS:
    name = request.META[ u'Shibboleth-eppn' ]
  elif settings_app.SPOOFED_ADMIN in settings_app.PERMITTED_ADMINS:
    name = settings_app.SPOOFED_ADMIN
  else:
    return HttpResponseForbidden()
  try:
    user = auth.models.User.objects.get( username=name )
    user.backend = u'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    return HttpResponseRedirect( u'../../admin/project_app/' )
  except:  # could auto-add user
    return HttpResponseForbidden()
