#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import boto3
from boto3.session import Session

if(len(sys.argv) != 2):
  print(sys.argv[0] + ' [start or stop] [InstanceID]')
  sys.exit()

try:
  session = Session(profile_name=sys.argv[1])
except Exception as e:
  print('\n' + 'Profile Errors: ' + str(e) + '\n')
  sys.exit()

region = 'ap-northeast-1'
client = session.client('ec2', region_name=region)


def ec2_control(instance_id, actions):
  if actions == 'start':
      client.start_instances(InstanceIds=sys.argv[2])
      ctrl_result = 'started your instance: ' + instance_id
  elif actions == 'stop':
      client.stop_instances(InstanceIds=sys.argv[2])
      ctrl_result = 'stopped your instance: ' + instance_id
  return ctrl_result


def get_status(instance_id):
   res = client.describe_instances(InstanceIds=sys.argv[2])
   status_result = res['Reservations'][0]['Instances'][0]['State']['Name']
   return status_result


def main():
  if(sys.argv[1] == 'stop' or sys.argv[1] == 'start'):
    print(ec2_control(sys.argv[2], sys.argv[1]))
  elif(sys.argv[1] == 'status'):
    print(get_status(sys.argv[2]))


if __name__ == '__main__':
  main()

