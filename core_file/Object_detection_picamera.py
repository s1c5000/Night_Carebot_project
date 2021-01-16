
# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys

# Set up camera constants
#IM_WIDTH = 1280
#IM_HEIGHT = 720
IM_WIDTH = 640    #크기를 줄이면 조금 빨라진다
IM_HEIGHT = 480   

# Select camera type

camera_type = 'picamera'


# 상위폴더로 접근을 위해서
sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# coco를 object detecting에 사용
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
#MODEL_NAME = 'faster_rcnn_resnet101_ava_v2.1_2018_04_30'

# 현재 작업 디렉토리에 대한 경로 확보
CWD_PATH = os.getcwd()

# 이미학습을 해놓은 pb파일을 객체감지에 사용, pb로 저장해놓은 모델은 속도가 빠른 장점이있다.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# label
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

# 클래스 갯수
NUM_CLASSES = 90

## Load the label map.
# 예측한 클래스값들을 문자열로 맵핑
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# 메모리에 모델 적제
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.compat.v1.Session(graph=detection_graph)


# object detection에 입력과 출력의 데이터정의

# Input tensor는 image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# output은 boxes, scores, classes
# 각 box는 특정 물체가 감지 된 이미지의 일부이다
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# 각 score는 개체에 대한 신뢰 수준
# 점수는 클래스 레이블과 함께 결과 이미지에 표시된다.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# 감지된 개체의 수
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# 프레임 정의
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX




# 카메라를 정의하고 object detection 실행

camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

numDetected=0

# 넘어짐 판단에 사용, 
# ymin, xmin, ymax, xmax
def is_fall(box):
    ymin = box[0]
    xmin = box[1]
    ymax = box[2]
    xmax = box[3]
    y_=ymax-ymin
    x_=xmax-xmin
    # fall
    if x_ >= y_ * 1.4:
        return True
    else:
        return False

for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

    t1 = cv2.getTickCount()
    
    # 프레임 크기를 확장시킨다 : [1, None, None, 3]
    frame = np.copy(frame1.array)
    frame.setflags(write=1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_expanded = np.expand_dims(frame_rgb, axis=0)

    # 실제 감지 수행
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})
    
    
    
    # 결과를 그린다.
    img, classes_,boxes_=vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=4,
        min_score_thresh=0.30) # line_thickness=8, min_score_thresh=0.40

    
    # 판단 상황을 볼수있게 출력, 3번이상 넘어짐판단이면 알람실행
    # ymin, xmin, ymax, xmax
    print('classes_:', classes_)
    
    for i,cls in enumerate(classes_):
        if cls=="person" and is_fall(boxes_[i]):
            numDetected += 1
            print('fall detected:', numDetected)
        
    if numDetected >= 3:
        print('fall counted 3 times')
        numDetected=0
        os.system('./detected.sh')


    cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

    # 모든 결과가 프레임에 그려진 뒤 show
    cv2.imshow('Object detector', frame)

    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1

    if cv2.waitKey(1) == ord('q'):
        break

    rawCapture.truncate(0)

camera.close()

cv2.destroyAllWindows()

