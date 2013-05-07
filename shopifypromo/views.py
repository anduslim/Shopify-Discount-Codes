from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
import requests
import re
import datetime
import json

ADMIN_URL = 'https://' + settings.SHOPIFY_STORE + '/admin'
LOGIN_URL = ADMIN_URL + '/auth/login'
COOKIE_STORE = '/tmp/shopify_cookie.txt'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
TOKEN = ''
DASHBOARD_TOKEN = ''
DATE_FORMAT = "%Y-%m-%d"
SESSION = requests.Session()

class LoginMixin(object):
    '''enables merchant login.
    '''

    def set_token(self, content):
        global TOKEN
        global DASHBOARD_TOKEN

        match = re.findall('meta content="(.*)" name="csrf-token"', content)
        if match:
            TOKEN = match[0]
            match = re.findall('Shopify.set\(\'controllers.dashboard.token\', "(.*)"\)', content)
            DASHBOARD_TOKEN = match[0]

    def get_tokens(self):
        return {'token' : TOKEN , 'dashboardtoken' : DASHBOARD_TOKEN}

    def login(self):
        username = settings.SHOPIFY_MERCHANT_EMAIL
        password = settings.SHOPIFY_MERCHANT_PASSWORD
        payload = {'login': 'anduslim@gozolabs.com', 'password': 'wolfen' }
        headers = {'Shopify-Auth-Mechanisms': 'password'}
        headers['Host'] = settings.SHOPIFY_STORE
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
        result = SESSION.post(LOGIN_URL, data=payload, headers=headers)
        self.set_token(result.content)
        return {'result' : result} 


class PromoCodeMixin(object):
    '''retrieve or update promo codes in shopify shop
    '''
    DISCOUNT_URL = ADMIN_URL + '/discounts.json'
    DEFAULT_KWARGS = { 'limit' : 50,
                        'order' : 'id',
                        'direction' : 'next'
                     }

    def get_promo_codes(self, **kwargs):
        if not kwargs:
            kwargs = self.DEFAULT_KWARGS 
        headers = {'token': DASHBOARD_TOKEN }
        result = SESSION.get(self.DISCOUNT_URL, params=kwargs)
        return {'promocode' : result}

    def set_promo_codes(self, new_promo_code):
        headers = {'X-CSRF-Token' : TOKEN}
        headers['X-Shopify-Api-Features'] = 'pagination-headers'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        result = SESSION.post(self.DISCOUNT_URL, data=json.dumps(new_promo_code), headers=headers)
        return {'newpromocode' : result }
        

class PromoCodeView(TemplateView, LoginMixin, PromoCodeMixin):
    '''View to display login auth details and promo codes
    ''' 
    # Create a default coupon
    DEFAULT_PROMO = {'discount' : {
        'applies_to_id' : '',
        'code' : 'DEFAULT',
        'discount_type' : 'percentage',
        'value' : 5,
        'usage_limit' : 1,
        'starts_at' : datetime.date.today().strftime(DATE_FORMAT),
        'ends_at' : None,
        'applies_once' : False
    }};
    template_name = 'promo_view.html'

    def get_context_data(self, **kwargs):
        context = super(PromoCodeView, self).get_context_data(**kwargs)
        context.update(self.login())
        context.update(self.get_tokens())
        context.update(self.get_promo_codes())
        context.update(self.set_promo_codes(self.DEFAULT_PROMO))
        return context

    def dispatch(self, *args, **kwargs):
        return super(PromoCodeView, self).dispatch(*args, **kwargs)