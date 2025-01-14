import numpy as np
import cv2
import os
import imutils

# load the COCO class labels our Mask R-CNN was trained on

#All 90 classes are listed in this text file, one per line.
# labelsPath = os.path.sep.join(["mask-rcnn-coco","object_detection_classes_coco.txt"])
# LABELS = open(labelsPath).read().strip().split("\n")
# #Mask R-CNN model weights. The weights are pre-trained on the COCO dataset
# weightsPath = os.path.sep.join(["mask-rcnn-coco","frozen_inference_graph.pb"])
# #Mask R-CNN model configuration
# configPath = os.path.sep.join(["mask-rcnn-coco", "mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"])
labelsPath = "mask-rcnn-coco/object_detection_classes_coco.txt"
LABELS = []
with open(labelsPath) as f:
    LABELS = f.read().strip().split("\n")
print(LABELS)
# load the set of colors that will be used when visualizing a given instance segmentation
colorsPath = "mask-rcnn-coco/colors.txt"
COLORS = []
with open(colorsPath) as f:
    COLORS = f.read().strip().split("\n")
COLORS = [np.array(c.split(",")).astype("int") for c in COLORS]
COLORS = np.array(COLORS, dtype="uint8")
print(COLORS)
# derive the paths to the Mask R-CNN weights and model configuration
weightsPath = "mask-rcnn-coco/frozen_inference_graph.pb"
configPath = "mask-rcnn-coco/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"

print("Loading Mask R-CNN from disk...")
net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)

#video
cam = cv2.VideoCapture('/home/vietthangtik15/dataset/input/video_1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out_video = cv2.VideoWriter('/home/vietthangtik15/dataset/output/output.avi',fourcc, 20.0, (2704,1520),True)
# for i in range(1,4):
while True:
    
    # path="images/person/"+str(i)+".jpg"
    # print(path)
    ret, img = cam.read()
    if ret == True:
    #grab a frame
        # src=cv2.imread(path)
        show = imutils.resize(img, width=500)
        #resize  it to a known width, maintaining aspect ratio
        frame = imutils.resize(img, width=1000)
        (H, W) = frame.shape[:2]
        
        #construct a blob  and complete a forward pass through the network
        blob = cv2.dnn.blobFromImage(frame, swapRB=True, crop=False)
        #print(blob)
        net.setInput(blob)
        #result is both boxes  and masks
        (boxes, masks) = net.forward(["detection_out_final", "detection_masks"])
        #print(boxes)
        print(boxes)
        #sorts the indexes of the bounding boxes by their corresponding prediction probability
        idxs = np.argsort(boxes[0, 0, :, 2])[::-1]
        #print(len(boxes))
        print("Detection Length",len(idxs))
        
        count=1

        for i in idxs:
            #extract the classID and confidence using boxes 
            classID = int(boxes[0, 0, i, 1])
            confidence = boxes[0, 0, i, 2]
            print(LABELS[classID])
            print(confidence)
            
            #for banana change the class label to banana    
            if LABELS[classID] == "person":
                #ensures the confidence  of the prediction exceeds the threshold
                if confidence > 0.8:
                    count=count+1

        print("Number of persons:",count-1)
        value="count="+str(count-1)
        #print the count on frames
        cv2.putText(show, value, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        # cv2.imshow("Output", show)
        out_video.write(show)
        # cv2.waitKey(0)
        
        # if cv2.waitKey(0) & 0xFF == ord('q'):
            # break
    else:
        break
    out_video.release()
cv2.destroyAllWindows()