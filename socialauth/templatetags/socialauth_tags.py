from django import  template

register = template.Library()

@register.simple_tag
def get_calculated_username(user):
    if hasattr(user, 'openidprofile_set') and user.openidprofile_set.filter().count():
        if user.openidprofile_set.filter(is_username_valid = True).count():
            return user.openidprofile_set.filter(is_username_valid = True)[0].user.username
        else:
            from django.core.urlresolvers import  reverse
            editprof_url = reverse('socialauth_editprofile')
            return u'Anonymous User. <a href="%s">Add name</a>'%editprof_url
    else:
        return user.username

@register.simple_tag
def get_calculated_first_name(user):
    if hasattr(user, 'openidprofile_set') and user.openidprofile_set.filter().count():
        if user.openidprofile_set.filter(is_username_valid = True).count():
            first_name =  user.openidprofile_set.filter(is_username_valid = True)[0].user.first_name
        else:
            first_name = ''

    else:
        first_name = user.first_name

        if not first_name:
            from django.core.urlresolvers import  reverse
            editprof_url = reverse('socialauth_editprofile')
            first_name = u'Anonymous User. <a href="%s">Add name</a>' % editprof_url

        return first_name

@register.inclusion_tag('socialauth/embedded_login.html')
def show_login(next):
    return {'next': next}
