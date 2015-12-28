import boto
import sys, os
from boto.s3.key import Key
import re
from boto.ec2.connection import EC2Connection
from boto.manage.cmdshell import sshclient_from_instance

LOCAL_PATH = '/'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

bucket_name = 'francis-iannacci-test-bucket'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(bucket_name)

# go through the list of files
bucket_list = bucket.list("raw_mp4/", "/")

def get_file_list(bucket_list, file_extension):
    '''
    '''
    files = []
    for l in bucket_list:
        keyString = str(l.key)
        if re.search("\." + file_extension, keyString):
            files.append(keyString)
    return files

def number_of_files(bucket_list, file_extension):
    '''
    '''
    total = 0
    for f in bucket_list:
        keyString = str(f.key)
        if re.search("\." + file_extension, f.key):
            total += 1
            #print f
    return total

class EC2Master(object):
    '''
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.conn = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        self.ec2_conn = boto.ec2.connect_to_region('us-west-2')
        self.instances = []

    def get_ec2_instance_list(self):
        '''
        '''
        reservations = self.ec2_conn.get_all_instances()
        for reservation in reservations:
            if reservation.instances[0].state == 'running':
                print "-I- Running instance:", reservation.instances[0].id
                self.instances.append(reservation.instances[0])
            else:
                print "-I- Instance ignored:", reservation.instances[0].id, reservation.instances[0].state
        return self.instances

    def get_instance(self, instance_name):
        '''
        '''
        return self.ec2_conn.get_all_instances([instance_name])[0].instances[0]

    def get_ssh_client(self, instance):
        '''
        '''
        return sshclient_from_instance(instance,
                                        ssh_key_file='/Users/fiannacci/.ssh/ec2_key.pem',
                                        user_name='ubuntu')

if __name__ == "__main__":
    ec2_conn = EC2Master()
    video_file_list = get_file_list(bucket_list, file_extension="mp4")
    num_files = len(video_file_list)
    instance_list = ec2_conn.get_ec2_instance_list()
    num_instances = len(instance_list)

    # number of files to process on each instance
    files_per_instance = int(num_files / num_instances) + 1
    print "Files per instance:", files_per_instance

    for i, instance_name in enumerate(instance_list):
        print instance_name
        ssh_client = ec2_conn.get_ssh_client(instance_name)

        ## Set environmental variables
        ssh_client.run('export AWS_ACCESS_KEY_ID=\''+ AWS_ACCESS_KEY_ID + '\'')
        ssh_client.run('export AWS_SECRET_ACCESS_KEY=\'' + AWS_SECRET_ACCESS_KEY + '\'')

        ## Create video directory
        ssh_client.run('mkdir /home/ubuntu/videos_to_process')

        ## Move files to each instance for processing
        #begin_index =  i * files_per_instance
        #end_index = (i+1) * files_per_instance - 1
        begin_index = 0
        end_index = 30
        for file_name in video_file_list[begin_index:end_index]:
            print bucket_name + '/' + file_name
            ssh_client.run('s3cmd get s3://' + bucket_name + '/' + file_name + ' /home/ubuntu/videos_to_process/')
            #break

        ## Process each video


        ##ssh_client = sshclient_from_instance(instance,
        ##                                     ssh_key_file='/Users/fiannacci/.ssh/ec2_key.pem',
        ##                                     user_name='ubuntu')
        #ssh_client.run('ls -al ./code/*.mp4 | wc -l')
        #status, stdout, stderr = ssh_client.run('ls -al')
        ##ssh_client.run('mkdir ~/videos_to_process')
