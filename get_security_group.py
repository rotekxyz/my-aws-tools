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

def get_vpc_id():
  vpc_desc = []
  res = client.describe_vpcs()
  for vpc_id_lists in res['Vpcs']:
    vpc_id = vpc_id_lists['VpcId']
    cidr_block = str(vpc_id_lists['CidrBlockAssociationSet'][0]['CidrBlock'])
    if 'Tags' in vpc_id_lists.keys():
      for vpc_tags in vpc_id_lists['Tags']:
        if 'Name' in vpc_tags['Key']:
          vpc_tag_name = vpc_tags['Value']
    else:
      vpc_tag_name = 'No Name Tag'
    vpc_desc.append([vpc_tag_name, vpc_id, cidr_block])
  return vpc_desc


def get_security_group(vpc_id):

  result = []
  dict_list = {}

  res = client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
  for sg_lists in res['SecurityGroups']:
    sec_grp_names = [sg_lists['GroupName'], sg_lists['Description'], sg_lists['GroupId']]
    sg_append_data = []
    if sg_lists['IpPermissions']:
      for sg_ip_Ingress in sg_lists['IpPermissions']:

        ingress_iprange_result = []
        sg_describe = []
        from_port = None
        ip_protocol = None
        prefix_ids = None
        ipv6_ranges = None
        to_prot = None
        cidr_ips = None
        ingress_iprange_desc = None
        ingress_iprange_cidr = None

        sec_rules = {}

        if 'FromPort' in sg_ip_Ingress.keys():
          from_port = sg_ip_Ingress['FromPort']
          if not from_port:
            from_port = ''
        if 'IpProtocol' in sg_ip_Ingress.keys():
          ip_protocol = sg_ip_Ingress['IpProtocol']
          if not ip_protocol:
            ip_protocol = ''
        if 'PrefixListIds' in sg_ip_Ingress.keys():
          prefix_ids = sg_ip_Ingress['PrefixListIds']
          if not prefix_ids:
            prefix_ids = ''
        if 'Ipv6Ranges' in sg_ip_Ingress.keys():
          ipv6_ranges = sg_ip_Ingress['Ipv6Ranges']
          if not ipv6_ranges:
            ipv6_ranges = ''
        if 'ToPort' in sg_ip_Ingress.keys():
          to_prot = sg_ip_Ingress['ToPort']
          if not to_prot:
            to_prot = ''

        for ingress_ip_range in sg_ip_Ingress['IpRanges']:
          if 'Description' in ingress_ip_range.keys():
            ingress_iprange_desc = ingress_ip_range['Description']
          ingress_iprange_cidr = ingress_ip_range['CidrIp']
          ingress_iprange_result.append([ingress_iprange_cidr, ingress_iprange_desc])

        for ingress_ip_range in sg_ip_Ingress['UserIdGroupPairs']:
          if 'GroupId' in ingress_ip_range.keys():
            ingress_iprange_grpid = ingress_ip_range['GroupId']
          ingress_iprange_result.append([ingress_iprange_grpid])

        sg_describe.append([from_port, ip_protocol, prefix_ids, ipv6_ranges, to_prot, cidr_ips])
        sec_rules = {"Desc": sg_describe, "ips": ingress_iprange_result}
        sg_append_data.append(sec_rules)

    else:
      print('None Rules')
    dict_list = {"Sec_Grp_Names": sec_grp_names, "rules": sg_append_data}
    result.append(dict_list)
  return result


def main():
  vpc_result = get_vpc_id()
  for vpc_result_lists in vpc_result:
    vpc_lists = ','.join(map(str,vpc_result_lists))
    result = get_security_group(vpc_lists.split(',')[1])
    print('####  VPC ID ########################################')
    print(vpc_lists.split(',')[1])
    print('')
    for sec_grp_lists in result:
      print('### Security Group Names ######################')
      print('## SG_Group Name')
      print('# groupname, desc, groupid')
      print(','.join(map(str,sec_grp_lists['Sec_Grp_Names'])))
      for sec_grp_desc in sec_grp_lists['rules']:
         print('## Security Plicy Desc')
         print('# from_port, ip_protocol, prefix_ids, ipv6_ranges, to_prot, cidr_ips')
         for sec_grp_rule in sec_grp_desc['Desc']:
           print(','.join(map(str,sec_grp_rule)))
         print('## Permit Src Ips')
         print('# ingress permit cidr, [desc]')
         for sec_grp_ips in sec_grp_desc['ips']:
           print(','.join(map(str,sec_grp_ips)))
         print('')


if __name__ == '__main__':
  main()


