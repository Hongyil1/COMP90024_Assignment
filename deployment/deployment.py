"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney
====================================================
"""

# !/usr/bin/env python

import argparse
import os
import sys
import time

import boto3
import paramiko
from ansible_playbook import run_playbook

num_of_instances = 1
instance_type = 'm2.tiny'
volume_size = 1
playbook_file_name = 'playbook.yml'
nectar_access_key_id = '295da0b55a534e33ac72c3b99106c592'
nectar_secret_access_key = '735993e0b7e546d8bb9e90c7508d8180'
private_key_file = os.path.expanduser('~/.ssh/team56')


def main():
    global ec2, num_of_instances, instance_type, volume_size

    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", help="no of nodes to deploy")
    parser.add_argument("--size", help="size of volumes to be attached in gb")
    parser.add_argument("--type", help="type of instance to be created")
    args = parser.parse_args()
    if args.nodes is not None:
        num_of_instances = args.nodes
    if args.size is not None:
        volume_size = args.size
    if args.type is not None:
        instance_type = args.type

    if not os.path.isfile(private_key_file):
        print(
            'error: private key not found')
        sys.exit(1)
    if not oct(os.stat(private_key_file).st_mode & 0o0077) == oct(0):
        print('error: please restrict to 600.')
        sys.exit(1)

    start_time = time.time()
    ec2 = establish_connection()
    print('connection established...\n')
    # print('creating instances...')
    # instances = create_instances(num_of_instances)
    #
    # print('\nattaching volumes...')
    # cont = False
    # while not cont:
    #     cont = True
    #
    #     for i in instances:
    #         i.load()
    #
    #         if i.state['Name'] == 'running':
    #             vols = i.volumes.all()
    #             volumes = [v for v in vols]
    #
    #             print('i-', i.id, ' volume count: ', len(volumes))
    #             if len(volumes) == 0:
    #                 try:
    #                     vol_info = create_volume(volume_size)
    #                 except:
    #                     print('failed to create volume')
    #                     continue
    #                 try:
    #                     attach_volume(vol_info, i)
    #                 except:
    #                     print(' - failed to attach volume')
    #                     continue
    #         else:
    #             cont = False
    #             break
    #
    #     if cont is False:
    #         print('instances are not ready - waiting')
    #         time.sleep(15)
    #
    # print('\nIP addresses')
    hosts = []
    hosts.append('115.146.86.247')
    # hosts.append('115.146.86.168')
    # hosts.append('115.146.85.135')
    #
    # for i in instances:
    #     print(i.id + ':' + i.private_ip_address)
    #     hosts.append(i.private_ip_address)

    print('\nchecking SSH tunnel')
    while True:
        if check_ssh(hosts) is True:
            break
        print('SSH not yet active on all instances - waiting...\n')
        time.sleep(15)

    print('\ndeploying to ' + str(hosts))
    pb_dir = os.path.dirname(os.path.abspath(__file__))
    playbook = "%s/%s" % (pb_dir, playbook_file_name)

    status, message = run_playbook(hosts, playbook=playbook, private_key_file=private_key_file)
    print(message + '\n')
    if status == 0:
        print('CouchDB admin utilities can now be accessed at the following URLs:')
        for h in hosts:
            print('http://{0}:5984/_utils/index.html'.format(h))
        print()

    print(" %s seconds " % (time.time() - start_time))
    sys.exit(status)


def create_volume(size):
    vol = ec2.create_volume(VolumeType='melbourne', Size=size, AvailabilityZone='melbourne-qh2')
    return vol


def attach_volume(vol_info, instance):
    vol_id = vol_info.id
    vol = ec2.Volume(vol_id)

    cont = False
    while not cont:
        cont = True
        vol.load()
        if vol.state == 'available':
            try:
                print('attaching', vol_id, ' to ', instance.id)
                # ec2.attach_volume(Device='/dev/vdb', InstanceId=instance.id, VolumeId=vol_id)
                instance.attach_volume(Device='/dev/vdb', VolumeId=vol_id)
                cont = True
            except:
                print('failed to attach volume')
                continue
        else:
            cont = False

        if cont is False:
            print('volume is not ready - waiting...')
            time.sleep(5)


def establish_connection():
    ec2 = boto3.resource(service_name='ec2', aws_access_key_id=nectar_access_key_id,
                         aws_secret_access_key=nectar_secret_access_key,
                         region_name='melbourne', endpoint_url='https://nova.rc.nectar.org.au:8773')
    return ec2


# def get_instance_ami_info():
#   for i in ec2.instances.all():
#     print("\tami Id: {1}\tplatform: {2}".format(
#         (i.image_id),
#         (i.platform)
#     ))


def create_instances(num):
    res = ec2.create_instances(ImageId='ami-86f4a44c', KeyName='team56', InstanceType=instance_type,
                               MinCount=num, MaxCount=num,
                               SecurityGroups=['team56_security'],
                               Placement={'AvailabilityZone': 'melbourne-qh2'})
    return res


def get_instances():
    return ec2.get_only_instances()


def print_instances():
    instances = get_instances()
    for i in instances:
        print(i.id + ':' + i.state)


class MissingKeyPolicy(paramiko.client.AutoAddPolicy):
    def missing_host_key(self, client, hostname, key):
        with open(os.path.expanduser('~/.ssh/known_hosts'), 'a') as f:
            f.write('%s %s %s\n' % (hostname, 'ssh-rsa', key.get_base64()))
        super(MissingKeyPolicy, self).missing_host_key(client, hostname, key)


def check_ssh(hosts):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(MissingKeyPolicy())
    client.load_system_host_keys()
    res = True
    for h in hosts:
        try:
            print(h)
            client.connect(h, username='ubuntu', key_filename=private_key_file)
            client.close()
            print('connection to ' + h + ' successful')
        except paramiko.ssh_exception.NoValidConnectionsError:
            print('unable to connect to ' + h)
            res = False
    return res


if __name__ == '__main__': main()
