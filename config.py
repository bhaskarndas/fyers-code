import pyotp
# update the userid for Fyers
USER_ID = 'ABDC000'

# add the client_id or app_key
CLIENT_ID='ABCDEF-100'

#Add the api_secret
API_SECRET = 'ABCDE'

#provide the redirect URI
REDIRECT_URI='https://www.bing.com'

#Provide TWOFA code from Fyers
TWOFA = ''

TOTP= pyotp.TOTP(TWOFA).now()
