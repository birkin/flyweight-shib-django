super lightweight shib-login in django
======================================

---

goal
====

Find the _simplest_ way to integrate [shib][shib] authentication into django's [authentication framework][dj_auth].

[shib]: http://shibboleth.net/
[dj_auth]: https://docs.djangoproject.com/en/dev/topics/auth/

Requirements:

- minimize project-level dependencies -- make it work at the app-level
- solution must work on non-shibbed development box

---

main part...
============

The views.login() code is fairly self-explanatory, but some notes...

- User-objects should have their passwords set to be unusable, so that a direct admin login will never work.

        from django.contrib.auth.models import User
        user = User( username=shib_eppn )
        user.set_unusable_password()
        user.save()

- There's a redundancy in the sample code: if authorization fails when a django user object doesn't exist, then the PERMITTED\_ADMINS setting isn't really needed. I have it as is to show an option: if you have a team of students, changing over time, it'd be easier to add/remove their usernames to the PERMITTED_ADMINS setting and let the except block auto add them & set their permissions.

- For those less familiar with django: When the redirect to the django admin happens, the user will bypass the normal django admin login screen because s/he's already logged in. Since django's user-framework is very flexible, one user at this point might see many admin tables with create/edit/delete privileges, while another might see only a few with only edit privileges.

- Historical note: in early versions of django, the symbols '@' and '.' were not valid username characters, requiring weird shib-eppn to django-username conversions like 'username\_at\_place\_dot_edu' -- progress!

---

supporting parts...
===================

settings_app.py
---------------

self-explanatory

project_httpd.conf
------------------

In our project/apache directory, in addition to the standard wsgi.py file, we use a project_httpd.conf file for three things:

- to direct the apache handoff to the wsgi.py file
- to specify the non-web directories apache will make web-accessible ( css, javascript, etc -- to version & deploy this stuff seamlessly )
- to configure shib-protected paths

The relevant shib section:

    <Location /the_project/the_app/login/>
      AuthType shibboleth
      ShibRequireSession On
      ShibUseHeaders On
      require valid-user
    </Location>
    
Note that this is using shib for authN, not authZ.

the link
--------

On one or more app webpages, have an 'admin' link that links to the app's shib-protected login page. (Make it an https link.)

---
