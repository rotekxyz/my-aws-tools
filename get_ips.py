#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

client = session.client('ec2')

def main():
  print('### Columns')
  print('## global_ip, instance_id, name, nw_owner, nw_if_id')
  addr_result = client.describe_addresses()
  for addr_lists in addr_result['Addresses']:
    if 'InstanceId' in addr_lists.keys():
      instance_id = addr_lists['InstanceId']
    else:
      instance_id = 'None'
    global_ip = addr_lists['PublicIp']
    if 'Tags' in addr_lists.keys():
      for names in addr_lists['Tags']:
        name = names['Value']
    else:
      name = 'No_Tag_Name'
    if 'NetworkInterfaceOwnerId' in addr_lists.keys():
      nw_id = addr_lists['NetworkInterfaceOwnerId']
    else:
      nw_id = 'No_Assign'

    if 'NetworkInterfaceId' in addr_lists.keys():
      if_id = addr_lists['NetworkInterfaceId']
    else:
      if_id = 'No_if_Assign'

    print(global_ip, instance_id, name, nw_id, if_id, sep='\t')

if __name__ == '__main__':
  main()


