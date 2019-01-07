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


def get_groups(username):
  group_lists = []
  res = iam.list_groups_for_user(UserName=username)
  for lists in res['Groups']:
    groupnames = lists['GroupName']
    group_lists.append(groupnames)
  return group_lists


def get_mfa_stats(username):
  res = iam.list_mfa_devices(UserName=username)
  if not res['MFADevices']:
    mfa_stats = 'MFA_False'
  else:
    mfa_stats = 'MFA_True'
  return mfa_stats


def get_avail_groups():
  avail_groups = []
  res = iam.list_groups()
  for lists in res['Groups']:
    avail_group = lists['GroupName']
    avail_groups.append(avail_group)
  return avail_groups


def get_policies(groupname):
  avail_policies = []
  res = iam.list_attached_group_policies(GroupName=groupname)
  for lists in res['AttachedPolicies']:
    avail_policy = lists['PolicyName']
    avail_policies.append(avail_policy)
  return avail_policies


def check_console_login(username):
  try :
    iam.get_login_profile(UserName=username)
    check_result = 'Login_Yes'
  except Exception :
    check_result = 'Login_No'
  return check_result


def main():
  print('### Userlists')
  for user_list in get_users():
    groupname = get_groups(user_list)
    mfa_stats = get_mfa_stats(user_list)
    console_login_stats = check_console_login(user_list)
    print(user_list, ':'.join(groupname), mfa_stats, console_login_stats, sep=',')
  print('\n### GroupLists')
  for group_list in get_avail_groups():
    policyname = get_policies(group_list)
    print(group_list, ':'.join(policyname), sep=',')


if __name__ == '__main__':
  main()

