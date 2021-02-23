from celery import shared_task
from core.models import Account

@shared_task
def hello(name):
    print(name)


# @shared_task
# def print_account_first_name(account_id):
#     account = Account.objects.filter(id=account_id).first()
#     print(account.user.first_name)

@shared_task
def get_fb_post(account_id):
    account = Account.objects.filter(id=account_id).first()
    print(account.user.first_name)
    







