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
<!DOCTYPE html>
<html>
<head>
    <title>搜索输入框demo</title>
    <link href="//vjs.zencdn.net/7.3.0/video-js.min.css" rel="stylesheet">
    <script src="//vjs.zencdn.net/7.3.0/video.min.js"></script>
</head>
<body>
    <video
        id="my-player"
        class="video-js vjs-big-play-centered"
        controls
        preload="auto"
        poster="//vjs.zencdn.net/v/oceans.png"
        data-setup='{}'>
      <source src="//vjs.zencdn.net/v/oceans.mp4" type="video/mp4"></source>
      <source src="//vjs.zencdn.net/v/oceans.webm" type="video/webm"></source>
      <source src="//vjs.zencdn.net/v/oceans.ogv" type="video/ogg"></source>
      <p class="vjs-no-js">
        To view this video please enable JavaScript, and consider upgrading to a
        web browser that
        <a href="https://videojs.com/html5-video-support/" target="_blank">
          supports HTML5 video
        </a>
      </p>
    </video>
</body>
<script type="text/javascript">
    var player = videojs('my-player');

    /*
    var options = {};

    var player = videojs('my-player', options, function onPlayerReady() {
      videojs.log('Your player is ready!');

      // In this context, `this` is the player that was created by Video.js.
      this.play();

      // How about an event listener?
      this.on('ended', function() {
        videojs.log('Awww...over so soon?!');
      });
    });
    */
</script>
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
