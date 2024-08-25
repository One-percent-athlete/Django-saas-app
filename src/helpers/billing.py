# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import stripe
from decouple import config as decouple_config

DJANGO_DEBUG=decouple_config('DJANGO_DEBUG', default=False, cast=bool)
STRIPE_SECRET_KEY=decouple_config('STRIPE_SECRET_KEY', default='', cast=str)

if 'sk_test' in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError('Invalid stripe key for prod.')

stripe.api_key = STRIPE_SECRET_KEY
stripe.Customer.create(
  name="Jenny Rosen",
  email="jennyrosen@example.com",
)