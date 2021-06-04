# MIT License
#
# Copyright (c) 2017 PXL University College
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Clusters similar faces from input folder together in folders based on euclidean distance matrix

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from scipy import misc
from shutil import copyfile
from sklearn.cluster import DBSCAN

import tensorflow as tf
import numpy as np
import os
import sys
import argparse
import facenet
import detect_face
import warnings
import time



def main(args):
	
	payloaddir = '/app/data/payloads'
	workdir = '/app/data/workdir'
	
    # Get rid of unnecessary warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    pnet, rnet, onet = create_network_face_detection(args.gpu_memory_fraction)

    with tf.Graph().as_default():
        with tf.Session() as sess:
            facenet.load_model(args.model)
            print("Ready to infer!")
            
            if args.loop == 'True':
                copyfile(payloaddir + '/facenet/payload.jpg', args.data_dir + '/payload.jpg')
            
            while True:
                if not os.path.exists(args.data_dir + "/payload.jpg"):
                    time.sleep(0.01)
                else:
                    t_start = time.time()
                    
                    for filename in os.listdir(workdir + '/face_database/'):
                        copyfile(workdir + '/face_database/' + filename, args.data_dir + "/" + filename)
                    image_list = load_images_from_folder(args.data_dir)
                    Path(args.temp_file).touch()
                    images = align_data(image_list, args.image_size, args.margin, pnet, rnet, onet)

                    images_placeholder = sess.graph.get_tensor_by_name("input:0")
                    embeddings = sess.graph.get_tensor_by_name("embeddings:0")
                    phase_train_placeholder = sess.graph.get_tensor_by_name("phase_train:0")
                    feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                    emb = sess.run(embeddings, feed_dict=feed_dict)

                    nrof_images = len(images)

                    matrix = np.zeros((nrof_images, nrof_images))

                    print('')
                    for i in range(nrof_images):
                        for j in range(nrof_images):
                            dist = np.sqrt(np.sum(np.square(np.subtract(emb[i, :], emb[j, :]))))
                            matrix[i][j] = dist

                    # DBSCAN is the only algorithm that doesn't require the number of clusters to be defined.
                    db = DBSCAN(eps=args.cluster_threshold, min_samples=args.min_cluster_size, metric='precomputed')
                    db.fit(matrix)
                    labels = db.labels_

                    # get number of clusters
                    no_clusters = len(set(labels)) - (1 if -1 in labels else 0)

                    largest_cluster = 0
                    for i in range(no_clusters):
                        if len(np.nonzero(labels == i)[0]) > len(np.nonzero(labels == largest_cluster)[0]):
                            largest_cluster = i
                    
                    t_total = time.time() - t_start
                    print('Image inferred in: {:.5f}s'.format(t_total))
                    
                    if largest_cluster > 0:
                        print('Match found! Person identified as ID: {}!'.format(largest_cluster))
                    else:
                        print('Match not found!')
                    print('')
                    
                    if args.loop == 'False':
                        for filename in os.listdir(args.data_dir):
                            os.remove(args.data_dir + "/" + filename)
                    
                    print('Ready to infer!')



def align_data(image_list, image_size, margin, pnet, rnet, onet):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    img_list = []

    for x in range(len(image_list)):
        img_size = np.asarray(image_list[x].shape)[0:2]
        bounding_boxes, _ = detect_face.detect_face(image_list[x], minsize, pnet, rnet, onet, threshold, factor)
        nrof_samples = len(bounding_boxes)
        if nrof_samples > 0:
            for i in range(nrof_samples):
                if bounding_boxes[i][4] > 0.95:
                    det = np.squeeze(bounding_boxes[i, 0:4])
                    bb = np.zeros(4, dtype=np.int32)
                    bb[0] = np.maximum(det[0] - margin / 2, 0)
                    bb[1] = np.maximum(det[1] - margin / 2, 0)
                    bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
                    bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
                    cropped = image_list[x][bb[1]:bb[3], bb[0]:bb[2], :]
                    aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
                    prewhitened = facenet.prewhiten(aligned)
                    img_list.append(prewhitened)

    if len(img_list) > 0:
        images = np.stack(img_list)
        return images
    else:
        return None


def create_network_face_detection(gpu_memory_fraction):
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
    return pnet, rnet, onet


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if not 'exec.tmp' in filename:
            img = misc.imread(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
    return images


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('model', type=str,
                        help='Either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    parser.add_argument('data_dir', type=str,
                        help='The directory containing the images to cluster into folders.')
    parser.add_argument('out_dir', type=str,
                        help='The output directory where the image clusters will be saved.')
    parser.add_argument('temp_file', type=str,
                        help='The temporary file.')
    parser.add_argument('loop', type=str,
						help='Set to True for infinite operation.')
    parser.add_argument('--image_size', type=int,
                        help='Image size (height, width) in pixels.', default=160)
    parser.add_argument('--margin', type=int,
                        help='Margin for the crop around the bounding box (height, width) in pixels.', default=44)
    parser.add_argument('--min_cluster_size', type=int,
                        help='The minimum amount of pictures required for a cluster.', default=1)
    parser.add_argument('--cluster_threshold', type=float,
                        help='The minimum distance for faces to be in the same cluster', default=1.0)
    parser.add_argument('--largest_cluster_only', action='store_true',
                        help='This argument will make that only the biggest cluster is saved.')
    parser.add_argument('--gpu_memory_fraction', type=float,
                        help='Upper bound on the amount of GPU memory that will be used by the process.', default=1.0)

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
