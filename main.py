"""People Counter."""
'''
AUTHOR: SWASTIK NATH.
IMPLEMENTATION IN COURTESY OF UDACITY
PROJECT 1: INTEL EDGE AI FOR IOT DEVELOPERS NANODEGREE
'''
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60


def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    return parser


def connect_mqtt():
    ### TODO: Connect to the MQTT client ###
    client = None

    return client


def infer_on_stream(args, client):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    current_request_num = 0
    total_count = 0
    current_count = 0
    single_image_mode = False
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    prob_threshold = args.prob_threshold

    ### TODO: Load the model through `infer_network` ###
    n,c,h,w = infer_network(args.model, args.device, 1, 1, current_request_num, args.cpu_extension)

    ### TODO: Handle the input stream ###
    if args.input.endswith('.jpg') or args.input.endswith('.bmp'):
        single_image_mode = True
        input_stream = args.input
    else:
        input_stream = args.input  #Handling the case of the Video Files
        assert os.path.isFile(args.input) "Error: Video File is not Found at the place specified."
    ### TODO: Loop until stream is over ###
    capture_frames = cv2.VideoCapture(input_stream)
    length_of_video = int(capture_frames.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(capture_frames.get(cv2.CAP_PROP_FPS))
        ### TODO: Read from the video capture ###
    infer_time_start = time.time()
    if input_stream:
        capture_frames.open(args.input)
    if not captures_frames.isOpened():
        log.error("Unable to Open the Video File.")
        
    global i_w, i_h
    i_w = capture_frames.get(3)
    i_h = capture_frames.get(4)
    
    while capture_frames.isOpened():
        isEnd, frame = capture_frames.read()
        current_count = 0
        if not isEnd:
            break
         ### TODO: Pre-process the image as needed ###
        inf_image = cv2.resize(frame, (w, h))
        inf_image = inf_image.transpose((2,0,1))
        inf_image = inf_image.reshape((n,c,h,w))

        ### TODO: Start asynchronous inference for specified request ###
        inf_start = time.time()
        infer_network.exec_net(current_request_num, inf_image)

        ### TODO: Wait for the result ###
        if infer_network.wait(current_request_num) == 0:
            duration = time.time() - inf_start
             ### TODO: Get the results of the inference request ###
            results = infer_network.get_output(current_request_num)
            ### TODO: Extract any desired stats from the results ###
            for det in results:
                if det[0][0] > prob_threshold:
                    current_count += 1 
                    total_count += current_count
                    
            ### TODO: Calculate and send relevant information on ###
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ###
            ### Topic "person/duration": key of "duration" ###

        ### TODO: Send the frame to the FFMPEG server ###

        ### TODO: Write an output image if `single_image_mode` ###
        if single_image_mode:
            cv2.imWrite('infer_out.jpg', frame)


def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
