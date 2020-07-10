# import the necessary packages
import numpy as np

# Malisiewicz et al.
# Python port by Adrian Rosebrock
# https://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/
def non_max_suppression_fast(boxes, overlapThresh): # boxes = an Numpy array containing rectangle coordiantes and scores, 5 for each rectangle
                                                    # overlapThresh = threshold for max proportion of overlap between rectangles. If two rectangles have a greater proportion of overlap than this, the one with the lower score will be filtered out. 
  # if there are no boxes, return an empty list
  if len(boxes) == 0:
    return []

  # initialize the list of picked indexes 
  pick = []

  # grab the coordinates of the bounding boxes
  x1 = boxes[:,0] # leftmost x coordinate
  y1 = boxes[:,1] # topmost y cooridnate
  x2 = boxes[:,2] # right x coordinate
  y2 = boxes[:,3] # bottommost y coordinate
  scores = boxes[:,4] # confidence score. higher score -> more confidence about detection


  # compute the area of the bounding boxes and sort the bounding
  # boxes by the score/probability of the bounding box
  area = (x2 - x1 + 1) * (y2 - y1 + 1)
  idxs = np.argsort(scores)[::-1]

  # keep looping while some indexes still remain in the indexes
  # list
  while len(idxs) > 0:
    # grab the last index in the indexes list and add the
    # index value to the list of picked indexes
    last = len(idxs) - 1
    i = idxs[last]
    pick.append(i)

    # find the largest (x, y) coordinates for the start of
    # the bounding box and the smallest (x, y) coordinates
    # for the end of the bounding box
    xx1 = np.maximum(x1[i], x1[idxs[:last]])
    yy1 = np.maximum(y1[i], y1[idxs[:last]])
    xx2 = np.minimum(x2[i], x2[idxs[:last]])
    yy2 = np.minimum(y2[i], y2[idxs[:last]])

    # compute the width and height of the bounding box
    w = np.maximum(0, xx2 - xx1 + 1)
    h = np.maximum(0, yy2 - yy1 + 1)

    # compute the ratio of overlap
    overlap = (w * h) / area[idxs[:last]]

    # delete all indexes from the index list that have
    idxs = np.delete(idxs, np.concatenate(([last],
      np.where(overlap > overlapThresh)[0]))) 

  # return only the bounding boxes that were picked
  return boxes[pick]
