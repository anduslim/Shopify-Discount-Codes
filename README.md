# Python Shopify Discount Code API Wrapper

---
#### Note: This is a python port of Martin's PHP Shopify Wrapper. All credits to him for discovering the 'hidden' API calls. For more information, refer to https://github.com/MartinAmps/Shopify-Private-APIs
---


## Requirements

refer to requirements.txt. To install dependencies, run `pip install -r requirements.txt`

## Usage

After cloning, 
1. Create a local_settings.py with
```python
from shopifyHack.settings import *
SHOPIFY_MERCHANT_EMAIL    = 'xyz@abc.xx'
SHOPIFY_MERCHANT_PASSWORD = 'abcxyz'
SHOPIFY_STORE = 'xyzabc.myshopify.com'
 ```

run ./manage.py runserver in your command console. Visit http://127.0.0.1:8000/promo/ for results. 


## Notes

Use at your own risk, enjoy!
