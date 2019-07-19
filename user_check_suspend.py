#!/usr/bin/env python3

import sys
import boto3
from boto3.session import Session
import datetime
from pytz import timezone


if(len(sys.argv) != 2):
  print(sys.argv[0] + ' [aws cli profile name]')
  sys.exit()


try:
  session = Session(profile_name=sys.argv[1])
except Exception as e:
  print('\n' + 'Profile Errors: ' + str(e) + '\n')
  sys.exit()


iam = session.client('iam')


def get_users():
  user_lists = []
  res = iam.list_users()
  for lists in res['Users']:
    userlist = lists['UserName']
    user_lists.append(userlist)
  return user_lists


def check_create_date(username):
  res = iam.get_user(UserName=username)
  create_date = res['User']['CreateDate']
  create_date = create_date.astimezone(timezone('Asia/Tokyo'))
  return create_date


def get_mfa_stats(username):
  res = iam.list_mfa_devices(UserName=username)
  if not res['MFADevices']:
    mfa_stats = 'MFA_False'
  else:
    mfa_stats = 'MFA_True'
  return mfa_stats


def check_console_login(username):
  try :
    iam.get_login_profile(UserName=username)
    check_result = 'Login_Yes'
  except Exception :
    check_result = 'Login_No'
  return check_result


def suspend_user(username):
    update_res = []
    delete_res = iam.delete_login_profile(UserName=username)
    update_res.append(delete_res)
    check_access_keys = iam.list_access_keys(UserName=username)
    for key_lists in check_access_keys['AccessKeyMetadata']:
      res = iam.update_access_key(UserName=username, AccessKeyId=key_lists['AccessKeyId'], Status='Inactive')
      update_res.append(res)
    return update_res


def main():
  print('### check start.')
  for user_list in get_users():
    mfa_stats = get_mfa_stats(user_list)
    console_login_stats = check_console_login(user_list)
    if 'MFA_False' in mfa_stats and 'Login_Yes' in console_login_stats:
      create_date = check_create_date(user_list)
      create_date = create_date.date()
      now_date = datetime.date.today()
      res_date = (now_date-create_date).days
      """
      var until_days is a duration of have not set MFA from account create day.
      """
      until_days = 7
      if until_days <= res_date:
        print(user_list + ' is Console Login YES. but have not set MFA for more than ' +
              str(res_date)  + 'days')
        result = suspend_user(user_list)
        #print(result)
    else:
      True
  print('### Finish')


if __name__ == '__main__':
  main()


