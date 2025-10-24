import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.test import Client
from farm.models import Farm

User = get_user_model()
username = 'testuserforfarm'
if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, password='password123')

client = Client()
client.defaults['HTTP_HOST'] = '127.0.0.1'
logged = client.login(username=username, password='password123')
print('logged in:', logged)

before = Farm.objects.filter(name='My Test Farm').count()
print('before count:', before)

resp = client.post('/farm/farms/create/', {'name':'My Test Farm','location':'Here','size_in_hectares':'12.5','crop_type':'Maize'}, follow=True)
print('POST status:', resp.status_code)

# print some diagnostics
try:
    form = resp.context.get('form') if resp.context else None
    if form:
        print('form errors:', form.errors)
    else:
        print('no form in context; maybe redirected or view returned other context')
except Exception as e:
    print('error retrieving form from context:', e)

after = Farm.objects.filter(name='My Test Farm').count()
print('after count:', after)

# show redirect chain
print('redirect chain:', resp.redirect_chain)
print('final url:', resp.request.get('PATH_INFO'))

# show response content snippet
print('response content snippet:', resp.content[:500])
