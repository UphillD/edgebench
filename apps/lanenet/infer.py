#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time	: 19-5-16 下午6:26
# @Author  : MaybeShewill-CV
# @Site	: https://github.com/MaybeShewill-CV/lanenet-lane-detection
# @File	: evaluate_lanenet_on_tusimple.py
# @IDE: PyCharm
"""
Evaluate lanenet model on tusimple lane dataset
"""
import argparse
import glob
import os
import os.path as ops
import time

import cv2
import numpy as np
import tensorflow as tf
import tqdm

from src.lanenet_model import lanenet
from src.lanenet_model import lanenet_postprocess
from src.config_utils import parse_config_utils
from src.log_util import init_logger

from pathlib import Path
from shutil import copyfile

CFG = parse_config_utils.lanenet_cfg
#LOG = init_logger.get_logger(log_file_name_prefix='lanenet_eval')


def init_args():
	"""

	:return:
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--image_dir', type=str, help='The source tusimple lane test data dir')
	parser.add_argument('--weights_path', type=str, help='The model weights path')
	parser.add_argument('--save_dir', type=str, help='The test output save root dir')
	parser.add_argument('--temp_file', type=str, help='The temporary file')
	parser.add_argument('--loop', type=str, help='Set to true for infinite operation')

	return parser.parse_args()


def eval_lanenet(src_dir, weights_path, save_dir, temp_file, loop):
	"""

	:param src_dir:
	:param weights_path:
	:param save_dir:
	:param temp_file:
	:return:
	"""

	tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
	os.makedirs(save_dir, exist_ok=True)

	input_tensor = tf.placeholder(dtype=tf.float32, shape=[1, 256, 512, 3], name='input_tensor')

	net = lanenet.LaneNet(phase='test', cfg=CFG)
	binary_seg_ret, instance_seg_ret = net.inference(input_tensor=input_tensor, name='LaneNet')

	postprocessor = lanenet_postprocess.LaneNetPostProcessor(cfg=CFG)

	saver = tf.train.Saver()

	# Set sess configuration
	sess_config = tf.ConfigProto()
	sess_config.gpu_options.per_process_gpu_memory_fraction = CFG.GPU.GPU_MEMORY_FRACTION
	sess_config.gpu_options.allow_growth = CFG.GPU.TF_ALLOW_GROWTH
	sess_config.gpu_options.allocator_type = 'BFC'

	sess = tf.Session(config=sess_config)

	with sess.as_default():

		saver.restore(sess=sess, save_path=weights_path)
		
		avgt = []
		temp = 0.0
		acet = 0.0
		wcet = 0.0
		cnt = 0
		
		print("Ready to infer.")
		
		while True:

			if loop == 'True':
				copyfile("/app/data/payloads/lanenet/payload.jpg", src_dir + '/payload.jpg')
                
			if not ops.exists(src_dir + "/payload.jpg"):
				time.sleep(0.01)
			else:
				
				Path(temp_file).touch()
				t_start = time.time()
				image_list = glob.glob('{:s}/**/*.jpg'.format(src_dir), recursive=True)

				for index, image_path in tqdm.tqdm(enumerate(image_list), total=len(image_list), disable=True):
					image = cv2.imread(image_path, cv2.IMREAD_COLOR)
					image_vis = image
					image = cv2.resize(image, (512, 256), interpolation=cv2.INTER_LINEAR)
					image = image / 127.5 - 1.0

					binary_seg_image, instance_seg_image = sess.run(
						[binary_seg_ret, instance_seg_ret],
						feed_dict={input_tensor: [image]}
					)

					postprocess_result = postprocessor.postprocess(
						binary_seg_result=binary_seg_image[0],
						instance_seg_result=instance_seg_image[0],
						source_image=image_vis
					)

					input_image_dir = ops.split(image_path)[0][1:]
					input_image_name = ops.split(image_path)[1]
					#output_image_dir = save_dir
					os.makedirs(save_dir, exist_ok=True)
					output_image_path = ops.join(save_dir, "output.jpg")
					#output_image_path = output_image_dir
					#if ops.exists(output_image_path):
					#	continue

					cv2.imwrite(output_image_path, postprocess_result['source_image'])
					
					t_total = time.time() - t_start
					
					avgt.append(t_total)
					
					cnt = cnt + 1
					
					if t_total > wcet:
						wcet = t_total
						
					if cnt % 10 == 0:
						acet = np.mean(avgt)
						print('ACET: {:.3f}s, WCET: {:.3f}s'.format(acet, wcet))
						avgt.clear()
						wcet = 0.0
					
					print('Image inferred in: {:.3f}s'.format(t_total))
					
					if loop == 'False':
						os.remove(image_path)
					os.remove(output_image_path)
					os.remove(temp_file)
					
					print("Ready to infer!")
					

	return


if __name__ == '__main__':
	"""
	test code
	"""
	# init args
	args = init_args()
	
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

	eval_lanenet(
		src_dir=args.image_dir,
		weights_path=args.weights_path,
		save_dir=args.save_dir,
		temp_file=args.temp_file,
		loop=args.loop
	)
