import base64
import hashlib
import hmac

channel_secret = 'a388fa7df47d6103e908e3cb8096f5d3' # Channel secret string
body = '...' # Request body string
hash = hmac.new(channel_secret.encode('utf-8'),
    body.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hash)
# Compare x-line-signature request header and the signature