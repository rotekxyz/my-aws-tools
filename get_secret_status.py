#!/usr/bin/env python3

import sys
import boto3
from boto3.session import Session

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


def get_cred_status(username):
  res = iam.list_access_keys(UserName=username)
  user_keys = []
  for lists in res['AccessKeyMetadata']:
    key_id = lists['AccessKeyId']
    key_status = lists['Status']
    key_create_date = lists['CreateDate']
    user_keys.append([key_id, key_status, key_create_date])
  return user_keys


def main():
  print('### UserNames & Credentials.')
  print('# CredentialId, Status, CreateDate.')
  for user_list in get_users():
    print('\n' + user_list + ' :')
    credential = get_cred_status(user_list)
    for credential_lists in credential:
      print(','.join(map(str,credential_lists )))


if __name__ == '__main__':
  main()

