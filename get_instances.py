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


def get_instance():
  intance_append_data = []
  res = client.describe_instances(Filters=[{'Name':'instance-state-name', 'Values':['running']}])
  for resrv_lists in res['Reservations']:
    for inst_lists in resrv_lists['Instances']:

      sec_grp_name = None
      sec_grp_apnd = []
      instance_id = None
      instance_type = None
      subnet_id = None
      ebs_detail = None
      ebs_detail_apnd = []
      pvt_ip = None
      pub_ip = None
      az = None
      vpc_id = None
      ssh_key_name = None
      detail_result = []

      if 'Tags' in inst_lists.keys():
        for inst_tags in inst_lists['Tags']:
          if 'Name' in inst_tags['Key']:
            instance_tag = inst_tags['Value']
      else:
        instance_tag = 'No Name Tag'
      for sec_grp_lists in inst_lists['SecurityGroups']:
        sec_grp_name = ([sec_grp_lists['GroupName'], sec_grp_lists['GroupId']])
        sec_grp_apnd.append(sec_grp_name)
      instance_id = (inst_lists['InstanceId'])
      instance_type = (inst_lists['InstanceType'])
      subnet_id = (inst_lists['SubnetId'])
      for ebs_lists in inst_lists['BlockDeviceMappings']:
        ebs_detail = ([ebs_lists['Ebs']['VolumeId'], ebs_lists['DeviceName']])
        ebs_detail_apnd.append(ebs_detail)
      for ntwk_lists in inst_lists['NetworkInterfaces']:
        for p_ip_lists in ntwk_lists['PrivateIpAddresses']:
          pvt_ip = (p_ip_lists['PrivateIpAddress'])
        if 'Association' in ntwk_lists:
          pub_ip = (ntwk_lists['Association']['PublicIp'])
        else:
          pub_ip = ('No Global IP')
      az = (inst_lists['Placement']['AvailabilityZone'])
      vpc_id = (inst_lists['VpcId'])
      if 'KeyName' in inst_lists:
        ssh_key_name = (inst_lists['KeyName'])
      else:
        ssh_key_name = ('No Key')
      detail_result.append([instance_tag,instance_id,instance_type,subnet_id,pvt_ip,pub_ip,az,vpc_id,ssh_key_name])
      result = {"instance": detail_result, "ebs":ebs_detail_apnd, "sec_grp": sec_grp_apnd}
      intance_append_data.append(result)
  return intance_append_data


def get_strages(volumeids):
  res = client.describe_volumes(VolumeIds=[volumeids])
  return res


def main():
  result = get_instance()
  for lists in result:
    print('### Instance Details ######################')
    print('## Instance Info')
    print('# instancename(tag), istance_id,instance_type,subnet_id,pvt_ip,pub_ip,az,vpc_id,ssh_key_name')
    for instances in lists['instance']:
      print(','.join(map(str,instances)))
    print('')
    print('## Attach EBS Info')
    print('# volumeid, devicename, volume size')
    for ebs_lists in lists['ebs']:
      vol_result = get_strages(ebs_lists[0])
      print(','.join(map(str,ebs_lists)) + ',' + str(vol_result['Volumes'][0]['Size'])  + 'G')
    print('')
    print('## Attach Security Group Info')
    print('# groupname, groupid')
    for sec_grp in lists['sec_grp']:
      print(','.join(map(str,sec_grp)))
    print('')


if __name__ == '__main__':
  main()


