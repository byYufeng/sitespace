#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('../libs')

import os
from flask import Flask, request
import json

demo = """
<html>
<head>
  <link href="https://vjs.zencdn.net/7.6.0/video-js.css" rel="stylesheet">

  <!-- If you'd like to support IE8 (for Video.js versions prior to v7) -->
  <script src="https://vjs.zencdn.net/ie8/1.1.2/videojs-ie8.min.js"></script>
</head>

<body>
  <video id='my-video' class='video-js' controls preload='auto' width='640' height='264'
  poster='MY_VIDEO_POSTER.jpg' data-setup='{}'>
    <source src='MY_VIDEO.mp4' type='video/mp4'>
    <source src='MY_VIDEO.webm' type='video/webm'>
    <p class='vjs-no-js'>
      To view this video please enable JavaScript, and consider upgrading to a web browser that
      <a href='https://videojs.com/html5-video-support/' target='_blank'>supports HTML5 video</a>
    </p>
  </video>

  <script src='https://vjs.zencdn.net/7.6.0/video.js'></script>
</body>
</html>
"""


app = Flask(__name__)

def main():
    debug = True
    host = '0.0.0.0'
    port = 8001 if len(sys.argv) < 2 else sys.argv[1]
    app.run(debug=debug, port=port, host=host)


@app.route('/')
def hello():
    return demo

if __name__ == '__main__':
    main()
