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

client = session.client('route53')


def get_hostedzones():
  results = []
  res = client.list_hosted_zones()
  for lists in res['HostedZones']:
    zonename = lists['Name']
    if lists['Config']['PrivateZone'] is True:
      private_zone = 'True'
    else:
      private_zone = 'False'
    if not lists['Config']['Comment']:
      conf_comment = ''
    else:
      conf_comment = lists['Config']['Comment']
    zoneid = lists['Id']
    results.append([zonename, private_zone, conf_comment, zoneid])
  return results


def get_records(zoneid):
  results = []
  res = client.list_resource_record_sets(HostedZoneId=zoneid)
  for lists in res['ResourceRecordSets']:
    rrs = []
    """
    replace char '\052' to '*'
    """
    if '\\052' in lists['Name']:
      rname = lists['Name'].replace('\\052', '*')
    else:
      rname = lists['Name']

    if 'TTL' in lists:
      ttl = str(lists['TTL'])
    rtype = lists['Type']
    if 'ResourceRecords' in lists:
      for rr_values in lists['ResourceRecords']:
        rrs.append(rr_values['Value'])
    results.append([rname, ttl, rtype, ' '.join(rrs)])
  return results


def main():
  for lists in get_hostedzones():
    print('\n' + '### Domain Info')
    print('# DOMAIN, PrivateFlag, COMMENT, DOMAIN ID')
    domain = ','.join(lists)
    print(domain)
    print('### RR')
    print('# hostname, ttl, rrtype, values')
    for lists in get_records(domain.split(',')[3]):
      print(','.join(lists))


if __name__ == '__main__':
  main()

