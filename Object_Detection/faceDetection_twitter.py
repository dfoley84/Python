#!/usr/bin/python3
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import tweepy
import subprocess
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from TwitterAPI import TwitterAPI
from twython import Twython


# Twitter Access Key
def login_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    ret = {}
    ret['api'] = api
    ret['auth'] = auth
    return api

def post_tweets():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    message = "Person Detection"
    api = login_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret)
    ret = api.update_status(status=message)

sys.path.append("..")

from utils import label_map_util
from utils import visualization_utils as vis_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME
DOWNLOAD_BASE = '/home/david/models/research/object_detection/'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


objects = []
function_person = False
threshold = 0.5

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
      while True:
          ret, image_np = cap.read()
          image_np_expanded = np.expand_dims(image_np, axis=0)
          image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
          boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
          scores = detection_graph.get_tensor_by_name('detection_scores:0')
          classes = detection_graph.get_tensor_by_name('detection_classes:0')
          num_detections = detection_graph.get_tensor_by_name('num_detections:0')

          (boxes, scores, classes, num_detections) = sess.run(
              [boxes, scores, classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})


          vis_util.visualize_boxes_and_labels_on_image_array(image_np,
          np.squeeze(boxes),np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),category_index,use_normalized_coordinates=True,
          line_thickness=1)

          for index, value in enumerate(classes[0]):
              object_dict = {}
              if scores[0, index] > threshold:
                  if (category_index.get(value).get('name') == 'person'):
                      if not function_person:
                          print('Hello')
                          function_person = True
