import numpy as np
import cv2
import imutils # Image processing library
import os # Operating system library 

cap = cv2.VideoCapture('sample_videos/occlusions-1.avi')
#ORIG_IMG_FILE = 'unstitched/boat03.jpg'
VIDEO_DIMENSIONS = (704, 576) # Dimensions that ENet was trained on
RESIZED_WIDTH = 600
IMG_NORM_RATIO = 1 / 255.0 # In grayscale a pixel can range between 0 and 255
while cap.isOpened():
    ret, frame = cap.read()
    input_img = imutils.resize(frame, width=RESIZED_WIDTH)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    input_img_blob = cv2.dnn.blobFromImage(input_img, IMG_NORM_RATIO,
    VIDEO_DIMENSIONS, 0, swapRB=True, crop=False)

    print("Loading the neural network...")
    enet_neural_network = cv2.dnn.readNet('./enet-cityscapes/enet-model.net')

    enet_neural_network.setInput(input_img_blob)

    enet_neural_network_output = enet_neural_network.forward()

    class_names = (open('./enet-cityscapes/enet-classes.txt').read().strip().split("\n"))

    (number_of_classes, height, width) = enet_neural_network_output.shape[1:4] 

    class_map = np.argmax(enet_neural_network_output[0], axis=0)

    if os.path.isfile('./enet-cityscapes/enet-colors.txt'):
        IMG_COLOR_LIST = (open('./enet-cityscapes/enet-colors.txt').read().strip().split("\n"))
        IMG_COLOR_LIST = [np.array(color.split(",")).astype("int") for color in IMG_COLOR_LIST]
        IMG_COLOR_LIST = np.array(IMG_COLOR_LIST, dtype="uint8")

    else:
        np.random.seed(1)
        IMG_COLOR_LIST = np.random.randint(0, 255, size=(len(class_names) - 1, 3), dtype="uint8")
        IMG_COLOR_LIST = np.vstack([[0, 0, 0], IMG_COLOR_LIST]).astype("uint8")    

    class_map_mask = IMG_COLOR_LIST[class_map]

    class_map_mask = cv2.resize(class_map_mask, (input_img.shape[1], input_img.shape[0]),interpolation=cv2.INTER_NEAREST)

    enet_neural_network_output = ((0.61 * class_map_mask) + (0.39 * input_img)).astype("uint8")
    
    class_legend = np.zeros(((len(class_names) * 25) + 25, 300, 3), dtype="uint8")

    for (i, (cl_name, cl_color)) in enumerate(zip(class_names, IMG_COLOR_LIST)):
        color_information = [int(color) for color in cl_color]
        cv2.putText(class_legend, cl_name, (5, (i * 25) + 17),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.rectangle(class_legend, (100, (i * 25)), (300, (i * 25) + 25),tuple(color_information), -1)

    combined_images = np.concatenate((input_img, enet_neural_network_output), axis=1) 


    cv2.imshow('frame', combined_images)
    cv2.imshow("Class Legend", class_legend)
    print(combined_images.shape)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()