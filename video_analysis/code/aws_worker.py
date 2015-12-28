import boto
import sys, os
from boto.s3.key import Key
import re
from os import listdir
from os.path import isfile, join
from video_feature_extraction import VideoFeatureExtraction

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

bucket_name = 'francis-iannacci-test-bucket'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(bucket_name)

## Get list of files in directory
path = '../videos_to_process/'
files = [f for f in listdir(path) if isfile(join(path, f))]

feature_extractor = VideoFeatureExtraction()
## run video analysis on each of them
for f in files:
    print f
    video_id = f.split('.')[0]
    video_path = join(path, f)
    print video_id, video_path
    feature_extractor.run(video_id, video_path)

    ## these file extensions should be referenced from the videdo_features file
    ## And so should the directory
    ## Also, should use "join" from the os.path module
    pkl_dir = "/home/ubuntu/code/"
    img_quality_file_path = pkl_dir + '/' + str(video_id) + '.img_quality.pkl'
    flow_file_path = pkl_dir + '/' + str(video_id) + '.flow.pkl'

    ## save off results to cloud
    ## TODO: creat the directories on EC2
    ssh_client.run('s3cmd put ' + img_quality_file_path + ' s3://' + bucket_name + '/' + 'img_quality/')
    ssh_client.run('s3cmd put ' + flow_file_path + ' s3://' + bucket_name + '/' + 'flow/')
