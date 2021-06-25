import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

firebase_admin_sdk = {
  "type": "service_account",
  "project_id": "quouze-57e1a",
  "private_key_id": "832cdc14065f5ccc5d231c1cf9e9c60388794850",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDongMq4YrnTtYp\nSfcFPW8c9xuuPbR730EgNHA2ux2kzuYWw6EqPHkrZ4JYZzj6J8Ub+uEF9w6tP9eF\nfJyDC7mTflxvb+mfpH4ogsjQGoQjQKNfA6KXHYZBru9J2qvRh49QHMnSKdAUwIRA\nepsSSDr7vAxQ2/0GC6G3wd3OnqfaMI0XLNDiSTf8MNuFmXAOMaTZoKJuyv2UYdMZ\nXd2Mk8ZiqTZR7Um1YlczNC2Gqw/pOUQMGNN1xg/QL/gE80yYLmC8fPLdZKKhnwCR\nL9sgDJrI9CupBBPEFgaiYos0XhvMqIj/F2pYuxRiofswg5BtKYi7rCFC3ZLR0mJn\n3ExEr9BZAgMBAAECggEAF8sd2NOEIT/LoSKLLVKI3IYcIzj1jpwZ7cDfX4HJOPPe\nziJJiGfyHvHx/7fjOJc7zq5dOP551lfK5EEIQ1E+NKt+qflhBK7PJral8r9bl72D\nWHMnPNzMwEgz+rJu07pReujO7fvP6Gd+v5eq5/ZSbjBgdB7kZStoacLfPMS2t5cA\n02KLGx47vv0Z6Xia6ZJ3E5gHHmRsSW3PfK3829HUhCWx7l8Vvuv8Oiv9Nsijy/Li\ny9fR+V19fXVciTtiWeWlYS5e3CVkt10d1oA1obEtnQwBt/33LXTrMALGgudEQqVd\nx3aOd/o8eRmR8OJN0KCMIxVWXTBybgqr9gB1AKks7wKBgQD090kDw1vqW4DgeX70\nzsvHehPsEHmLMkoPi09Q5+IiHIjJX6mu/TT+uf/dS1QzlLnoN30eEZEU6rJs6OE0\n0DBlHLwEd8f29jzvGeRugCRb9MV/em84QNgVmRbT2ei8al3Wo/4UR7sL7rSEEmUC\nXAKdNAL0P7qGG3NmK2/wWquJuwKBgQDzGFVbStTUSvCZqZ0EEnRBnfwVHk/RIsCt\nVEwDXHimn5hueKtvkMuiIlDr3FSkg3GjtmpWUBUslRHtTyHmZGBPHJ9EHIv32MIM\ncI1tz+/o5R1TGyym/JV3GfxbzrbcSNCb+835CWSHfq0YnucFQey1vFfzJ6cfLV01\nm78E25fy+wKBgQCkfZRq0XjcArukgBDvBBm0BdZw0pM7E/bFP09wTXT8YNq9Fd6U\nIXS/g1g7WcTdqgW31+LNGRCp0fsjxLDMzOtiSgw6l9APlkNObr2EMcm4ccFYm3cp\nd+lhf13jvdRZCLegVJhdN9ly5sQSV2O6VNxwgSdmqZBvUumHdq2A4PGE1wKBgQCA\nqAc8ysz7EjJmURNNvWqT88YfcyxxFgB9e5jDSqR8IwkspmatJCfxxlGnkrOlYf+5\n0mhTCA08zCRxwSjC46rpE8/i32zgnnKM3OCtFpj1XJT5j+9A7Xs5TqJ2AGBdE5h8\nhXcMb4EqCMwZtLe1258oy+aMRRc48+xZ2/Tr4EB6EwKBgQCqwylcJAvCy4r45Am2\nVBip7xVXo7VFsnp4UbSzSlnPVZDwolZ4/BjlnXtir5YtiantfzCrBG2wbsRBIHxq\nS43GxNtYmkCtSvQLT8ZQ9E7HwwXNMjotxAod3t1/3l/DFaAXcZIEnprSTS5qssXf\nmtUMXGhkSqQqSLTCLJKKvdMFWw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-4vq80@quouze-57e1a.iam.gserviceaccount.com",
  "client_id": "118246523264564474499",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4vq80%40quouze-57e1a.iam.gserviceaccount.com"
}


cred = credentials.Certificate(firebase_admin_sdk)
firebase_admin.initialize_app(cred)

# This registration token comes from the client FCM SDKs.
registration_token = 'eQhr2UaSOkoYlFRAjMumvH:APA91bEuh3x599x2eXVcJL_hP_rMRrtvbdVmcohmoEkBAkFa8WHBk57x-QONGKZb0OLlvwkslqjT4vA0b-Y_FRg_6hEz0YBAVjtMDu1F21pqLB6fVdrVTs9I9jrJB-pn87ktjZXTfQQL'

# See documentation on defining a message payload.
message = messaging.Message(
    notification=messaging.Notification(
        title='test server',
        body='test server message',
    ),
    token=registration_token,
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)