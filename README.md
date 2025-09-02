# 2025-gtsolar-trackviz
Visualization of GTSolar Track file

## Heading offset problem

When you zoom way into the track, you'll see the lat/long/heading plotted atop the track itself. Note: In order to zoom, you may need to maximize the window so the zoom button appears. Also, if dragging out a zoom view doesn't work, try again.

On lines 55-56 of TrackViz.py, you'll find a shifting of the heading which makes the whiskers line up with the track. If you comment-out lines 55-56, you'll see that the headings do not follow the track; they are off by one point.