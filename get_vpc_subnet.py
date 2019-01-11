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


def get_subnets(vpc_id):
  subnet_desc = []
  res = client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
  for subnet_lists in res['Subnets']:
    subnet_id = subnet_lists['SubnetId']
    az = subnet_lists['AvailabilityZone']
    cb = subnet_lists['CidrBlock']
    if not subnet_lists['Ipv6CidrBlockAssociationSet']:
      ipv6_cb = ''
    else:
      ipv6_cb = subnet_lists['Ipv6CidrBlockAssociationSet']
    if 'Tags' in subnet_lists.keys():
      for subnet_tags in subnet_lists['Tags']:
        if 'Name' in subnet_tags['Key']:
          subnet_tag = subnet_tags['Value']
        else:
          subnet_tag = 'No Name Tag'
    else:
      subnet_tag = 'No Name Tag'
    subnet_desc.append([subnet_tag, subnet_id, az, cb, ipv6_cb])
  return subnet_desc


def get_route_tables(vpc_id):
  associate_append = []
  gw_id_append = []
  route_append = []
  count_append = []

  res = client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
  for lists in res['RouteTables']:
    associate_append = []
    gw_id_append = []
    route_append = []

    for Associations_lists in lists['Associations']:
      asso_mode = Associations_lists['Main']
      asso_id = Associations_lists['RouteTableAssociationId']
      asso_table_id = Associations_lists['RouteTableId']
      if 'SubnetId' in Associations_lists.keys():
        asso_subnet_id = Associations_lists['SubnetId']
      else:
        asso_subnet_id = ''
      associate_append.append([asso_mode,asso_id,asso_table_id,asso_subnet_id])
    for gw_lists in lists['PropagatingVgws']:
      gw_id_append.append(gw_lists['GatewayId'])
    for route_lists in lists['Routes']:
      dest_cidr = route_lists['DestinationCidrBlock']
      if 'GatewayId' in route_lists.keys():
        gw_ids = route_lists['GatewayId']
      else:
        gw_ids = ''
      route_origin = route_lists['Origin']
      route_append.append([dest_cidr, gw_ids, route_origin])
    if 'Tags' in Associations_lists.keys():
      for subnet_tags in Associations_lists['Tags']:
        if 'Name' in subnet_tags['Key']:
          subnet_tag = subnet_tags['Value']
    else:
      subnet_tag = 'No Name Tag'
    append_dict = {"associate_desc": associate_append, "gw_ids": gw_id_append, "route_desc": route_append, "tags": subnet_tag}
    count_append.append(append_dict)
  return count_append


def main():
  vpc_result = get_vpc_id()
  print('#### VPC and Subnet Info')
  for vpc_result_lists in vpc_result:
    print('## VPC Description')
    print('# vpc tag name, vpcid, ciderblock')
    vpc_lists = ','.join(map(str,vpc_result_lists))
    print(vpc_lists)
    print('## SubnetDescription')
    print('# subnet tag name, subnetid, az, ciderblock, ipv6 ciderblock')
    subnet_result = get_subnets(vpc_lists.split(',')[1])
    for subnet_result_lists in subnet_result:
      print(','.join(map(str,subnet_result_lists)))
    print('')


if __name__ == '__main__':
  main()

