import cv2, os
import matplotlib.pyplot as plt
import numpy as np


import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    try:
        # Restrict TensorFlow to only use the fourth GPU
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
save_dir = './insta_image3' # 저장할 폴더명

gender_list = ['Male', 'Female']
gender_net = cv2.dnn.readNetFromCaffe(
          './deploy_gender.prototxt',
          './gender_net.caffemodel')

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

def search(dirname):
    img_list = []
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.jpg':
                img_list.append(path+'/'+filename)
    return img_list

image_list = search('C:\\Users\\USER\\PycharmProjects\\pythonProject1\\img2')

print(image_list[0])
img_array = []
image_frame = []
face = []

image_size =[]
cut_image = []
count = 0

for i in range(len(image_list)):
# for i in range(0, 100):
    img_array.append(np.fromfile(image_list[i], np.uint8))
    image_frame.append(cv2.imdecode(img_array[i], cv2.IMREAD_COLOR))
    face.append(face_cascade.detectMultiScale(image_frame[i],1.3,5))
    print(i)
    if len(face[i]) !=0 :
        for (x,y,w,h) in face[i] :
            if (x > 25 and y > 25) :
                cut_image.append(image_frame[i][y-25:y+w+25, x-25:x+h+25].copy())

for i in range(len(cut_image)):
    print(i)
    width,height,channel = cut_image[i].shape
    blob = cv2.dnn.blobFromImage(cut_image[i], scalefactor=1, size=(227, 227),
        mean=(78.4263377603, 87.7689143744, 114.895847746),
        swapRB=False, crop=False)
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = gender_list[gender_preds[0].argmax()]
    if (width >= 300):
        if gender == 'Male':
            cv2.imwrite('./male'+'/'+str(i)+'.jpg',cut_image[i])
        else :
            cut_image[i] = cv2.resize(cut_image[i],dsize=(300,320))
            cv2.imwrite('./insta_image3'+'/'+str(i)+'.jpg',cut_image[i])
        count += 1
print(count)