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

client = session.client('elb')


def get_loadbalancer():
  result = []
  lb_append_data = []

  res = client.describe_load_balancers()
  for lb_lists in res['LoadBalancerDescriptions']:

    listen_desc_append = []
    az_append = []
    subnet_append = []
    instance_append = []
    sec_group_append = []
    lb_append = []

    # names
    lb_name = lb_lists['LoadBalancerName']
    dns_name = lb_lists['DNSName']
    if 'CanonicalHostedZoneName' in lb_lists:
      hosted_name = lb_lists['CanonicalHostedZoneName']
    else:
      hosted_name = "---"
    hosted_name_id = lb_lists['CanonicalHostedZoneNameID']
    # Listen Descriptions
    for listen_desc in lb_lists['ListenerDescriptions']:
      listen_prot = listen_desc['Listener']['Protocol']
      listen_port = listen_desc['Listener']['LoadBalancerPort']
      listen_to_prot = listen_desc['Listener']['InstanceProtocol']
      listen_to_port = listen_desc['Listener']['InstancePort']
      if 'PolicyNames' in listen_desc['Listener']:
        policy_name = listen_desc['Listener']['PolicyNames']
      else:
        policy_name = ''
      listen_desc_append.append([listen_prot,listen_port,listen_to_prot,listen_to_port,policy_name])
    # Availability Zones
    for az_lists in lb_lists['AvailabilityZones']:
       az_append.append(az_lists)
    # Network Info
    for sub_lists in lb_lists['Subnets']:
       subnet_append.append(sub_lists)
    vpc_id = lb_lists['VPCId']
    for instance_lists in lb_lists['Instances']:
      instance_append.append(instance_lists['InstanceId'])
    health_target = str(lb_lists['HealthCheck']['Target'])
    health_interval = str(lb_lists['HealthCheck']['Interval'])
    health_timeout = str(lb_lists['HealthCheck']['Timeout'])
    health_un_thresh = str(lb_lists['HealthCheck']['UnhealthyThreshold'])
    health_thresh = str(lb_lists['HealthCheck']['HealthyThreshold'])
    for sec_groups in lb_lists['SecurityGroups']:
      sec_group_append.append(sec_groups)

    lb_append.append([lb_name, dns_name, hosted_name, hosted_name_id, vpc_id, health_target, \
                   health_target ,health_timeout, health_un_thresh, health_un_thresh])
    result = {"lb_detail": lb_append, "listen_details": listen_desc_append, "az_details": az_append, \
              "subnet_details": subnet_append,"instance_details": instance_append,"sec_grouop_details": sec_group_append}
    lb_append_data.append(result)
  return lb_append_data


def main():
  for result_lists in get_loadbalancer():
    print('### AWS LBs ')
    for lb_detail_result in result_lists['lb_detail']:
      print('# lb_name, dns_name, hosted_name, hosted_name_id, vpc_id, health_target, health_target ,health_timeout,\
 health_un_thresh, health_unhealthy_thresh')
      print(','.join(map(str,lb_detail_result)))
    for listen_detail_result in result_lists['listen_details']:
      print('# listen_prot,listen_port,listen_to_prot,listen_to_port,policy_name')
      print(','.join(map(str,listen_detail_result)))
    print('# availability zones info')
    print(','.join(map(str,result_lists['az_details'])))
    print('# subnet info')
    print(','.join(map(str,result_lists['subnet_details'])))
    print('# instance info')
    print(','.join(map(str,result_lists['instance_details'])))
    print('# Inbound Security Group info')
    print(','.join(map(str,result_lists['sec_grouop_details'])))
    print('')


if __name__ == '__main__':
  main()

