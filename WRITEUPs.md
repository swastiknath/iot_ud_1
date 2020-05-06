# Udacity | Intel (R) Edge AI for IoT Developers Nanodegree
# CAPS 1: DEPLOY A PEOPLE COUNTER APP AT THE EDGE

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

## Explaining Custom Layers

The Custom layers of certain Single Shot Detection models which are transformed into Intermediate Representation are certainly the layers those do all the post processing. CPU cannot process the calculations by default without using a custom layer library. In this case they are the following layers:

  - DetectionOutput: which provides number, confidence and co-ordinates of the bounding boxes in (xmin, ymin) and (xmax, ymax) format. 
  
  - PriorBoxClustered: which are actually different bounding boxes drawn acorss the detected object across different sliding windows. These PriorBoxClustered Layers are later concatenated together, resized and presented as Detection Output. 
  
### Reasons for handling Custom Layers:
In order to draw the bounding boxes only with the detected objects where detection confidence is greater than a pre-specified threshold the Intermediate Representation uses **PriorBoxClustered** and **DetectionOutput** custom layers. In this scenario, we are also aiming to produce a model which can go ahead and detect persons in every frame of a video. 

### Handling the Custom Layers:
We can handle the above said custom layers using the **MKLDNN** Library for CPU which is available with OpenVino Installation at the following location:
```
<INSTALL_DIR>/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so
```
We add the above said library as an extension to the **IECore()** object of the model before actually loading the IR files. 

## Comparing Model Performance:

My method(s) to compare models before and after conversion to Intermediate Representations
were...

The difference between model accuracy pre- and post-conversion was...

The size of the model pre- and post-conversion was...

The inference time of the model pre- and post-conversion was...

## Assess Model Use Cases

### Use Cases of the People Counter Application:

 - Security: We can deploy the people counter application along with the security cameras to look for intruders. We can detect mobbing or stampede too as the application sends out a message to the MQTT if the current count of people in the frame is greater than a specified number. 
 
 - Smart Queing Systems: We can use this application as a baseline to create an application that can perform smart queing based on the number of people in the current frame. 
 
 - Counting the Total Number of People in a Place: We can deploy the application in a surveillance camera. By feeding the footage from the camera we will be able to count the total number of people on a public gathering like a festival, or a stadium etc.
 
 - Airline Boarding: We can use this application in a airline boarding place where we can measure the average duration of boading of a passanger to an aircraft and scrutinize in case of delay and use these telemetry to evaluate the customer satisfaction. 

As the application is opensource, further modifications can be made to adapt to further different use cases than the ones described earlier. 

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows...

### Efficiency Scenario for Model Accuracy:

The models specifically the ones from the Tensorflow OpenModel Zoo are pre-trained and are used here with their freezed inference graph, with no retraining or whatsoever. The ones with SSD Inception, SSD MobileNet and SSDLite were trained with COCO Image dataset along with different objects. So, the performance is quite a big issue here. In few of the frames while using these models we were able to see that the models are unable to detect the person standing backwards. We must say, in order to improve the accuracy we must train it with our own dataset in compliance with the Transfer Learning. 

### Efficiency Scenario for Lightning Conditions, Camera Focal Lenth / Image Size:

The original camera feed image size is not ofcourse a problem, beacuse we have addressed that issue by getting the model's input size prioritites and have applied the resize transformation over the images. However with higher resolution videos frame by frame resizing becomes computationally expensive and takes a significant amount of time. 

As discussed earlier the models are pretrained and proper lighting is needed in order to parse people from the images. With insufficient the model will fail to detect people in the frame. 

The camera focal length will also play a signifacnt role, if the image is outfocused the model will not be able to detect any person entering or exiting the frames. 


## Model Research

[This heading is only required if a suitable model was not found after trying out at least three
different models. However, you may also use this heading to detail how you converted 
a successful model.]

In investigating potential people counter models, I tried each of the following three models:

- Model 1: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
  
- Model 2: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

- Model 3: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
