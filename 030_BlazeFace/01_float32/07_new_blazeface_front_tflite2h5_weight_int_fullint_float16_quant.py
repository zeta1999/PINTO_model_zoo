### tensorflow==2.3.0

### https://ai.googleblog.com/2020/08/on-device-real-time-body-pose-tracking.html
### https://google.github.io/mediapipe/solutions/pose

### https://www.tensorflow.org/api_docs/python/tf/keras/Model
### op types: ['CONV_2D', 'RELU', 'DEPTHWISE_CONV_2D', 'ADD', 'MAX_POOL_2D', 'RESHAPE', 'CONCATENATION']

### https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/DepthwiseConv2D
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/Add
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/ReLU
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPool2D
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/Reshape
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/Concatenate
### https://www.tensorflow.org/api_docs/python/tf/keras/layers/Layer

### How to initialize a convolution layer with an arbitrary kernel in Keras? https://stackoverrun.com/ja/q/12269118

###  saved_model_cli show --dir saved_model_face_detection_front/ --tag_set serve --signature_def serving_default

import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Conv2D, DepthwiseConv2D, Add, ReLU, MaxPool2D, Reshape, Concatenate, Layer
from tensorflow.keras.initializers import Constant
import numpy as np
import sys
import tensorflow_datasets as tfds

# tmp = np.load('weights/depthwise_conv2d_Kernel')
# print(tmp.shape)
# print(tmp)

# def init_f(shape, dtype=None):
#        ker = np.load('weights/depthwise_conv2d_Kernel')
#        print(shape)
#        return ker

# sys.exit(0)

inputs = Input(shape=(128, 128, 3), batch_size=1, name='input')

# Block_01
conv1_1 = Conv2D(filters=24, kernel_size=[5, 5], strides=[2, 2], padding="same", dilation_rate=[1, 1], activation='relu',
                 kernel_initializer=Constant(np.load('weights_front/conv2d_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_Bias')))(inputs)
depthconv1_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_Bias')))(conv1_1)
conv1_2 = Conv2D(filters=24, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_1_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_1_Bias')))(depthconv1_1)
add1_1 = Add()([conv1_1, conv1_2])
relu1_1 = ReLU()(add1_1)

# Block_02
depthconv2_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_1_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_1_Bias')))(relu1_1)
conv2_1 = Conv2D(filters=28, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_2_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_2_Bias')))(depthconv2_1)
pad2_1 = tf.pad(relu1_1, paddings=tf.constant(np.load('weights_front/channel_padding_Paddings')))
add2_1 = Add()([conv2_1, pad2_1])
relu2_1 = ReLU()(add2_1)

# Block_03
depthconv3_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[2, 2], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_2_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_2_Bias')))(relu2_1)
conv3_1 = Conv2D(filters=32, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_3_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_3_Bias')))(depthconv3_1)
maxpool3_1 = MaxPool2D(pool_size=[2, 2], strides=[2, 2], padding='same')(relu2_1)
pad3_1 = tf.pad(maxpool3_1, paddings=tf.constant(np.load('weights_front/channel_padding_1_Paddings')))
add3_1 = Add()([conv3_1, pad3_1])
relu3_1 = ReLU()(add3_1)

# Block_04
depthconv4_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_3_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_3_Bias')))(relu3_1)
conv4_1 = Conv2D(filters=36, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_4_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_4_Bias')))(depthconv4_1)
pad4_1 = tf.pad(relu3_1, paddings=tf.constant(np.load('weights_front/channel_padding_2_Paddings')))
add4_1 = Add()([conv4_1, pad4_1])
relu4_1 = ReLU()(add4_1)

# Block_05
depthconv5_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_4_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_4_Bias')))(relu4_1)
conv5_1 = Conv2D(filters=42, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_5_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_5_Bias')))(depthconv5_1)
pad5_1 = tf.pad(relu4_1, paddings=tf.constant(np.load('weights_front/channel_padding_3_Paddings')))
add5_1 = Add()([conv5_1, pad5_1])
relu5_1 = ReLU()(add5_1)

# Block_06
depthconv6_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[2, 2], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_5_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_5_Bias')))(relu5_1)
conv6_1 = Conv2D(filters=48, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_6_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_6_Bias')))(depthconv6_1)
maxpool6_1 = MaxPool2D(pool_size=[2, 2], strides=[2, 2], padding='same')(relu5_1)
pad6_1 = tf.pad(maxpool6_1, paddings=tf.constant(np.load('weights_front/channel_padding_4_Paddings')))
add6_1 = Add()([conv6_1, pad6_1])
relu6_1 = ReLU()(add6_1)

# Block_07
depthconv7_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_6_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_6_Bias')))(relu6_1)
conv7_1 = Conv2D(filters=56, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_7_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_7_Bias')))(depthconv7_1)
pad7_1 = tf.pad(relu6_1, paddings=tf.constant(np.load('weights_front/channel_padding_5_Paddings')))
add7_1 = Add()([conv7_1, pad7_1])
relu7_1 = ReLU()(add7_1)

# Block_08
depthconv8_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_7_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_7_Bias')))(relu7_1)
conv8_1 = Conv2D(filters=64, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_8_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_8_Bias')))(depthconv8_1)
pad8_1 = tf.pad(relu7_1, paddings=tf.constant(np.load('weights_front/channel_padding_6_Paddings')))
add8_1 = Add()([conv8_1, pad8_1])
relu8_1 = ReLU()(add8_1)

# Block_09
depthconv9_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_8_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_8_Bias')))(relu8_1)
conv9_1 = Conv2D(filters=72, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_9_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_9_Bias')))(depthconv9_1)
pad9_1 = tf.pad(relu8_1, paddings=tf.constant(np.load('weights_front/channel_padding_7_Paddings')))
add9_1 = Add()([conv9_1, pad9_1])
relu9_1 = ReLU()(add9_1)

# Block_10
depthconv10_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_9_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_9_Bias')))(relu9_1)
conv10_1 = Conv2D(filters=80, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_10_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_10_Bias')))(depthconv10_1)
pad10_1 = tf.pad(relu9_1, paddings=tf.constant(np.load('weights_front/channel_padding_8_Paddings')))
add10_1 = Add()([conv10_1, pad10_1])
relu10_1 = ReLU()(add10_1)

# Block_11
depthconv11_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_10_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_10_Bias')))(relu10_1)
conv11_1 = Conv2D(filters=88, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_11_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_11_Bias')))(depthconv11_1)
pad11_1 = tf.pad(relu10_1, paddings=tf.constant(np.load('weights_front/channel_padding_9_Paddings')))
add11_1 = Add()([conv11_1, pad11_1])
relu11_1 = ReLU()(add11_1)

# Block_12
depthconv12_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[2, 2], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_11_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_11_Bias')))(relu11_1)
conv12_1 = Conv2D(filters=96, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_12_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_12_Bias')))(depthconv12_1)
maxpool12_1 = MaxPool2D(pool_size=[2, 2], strides=[2, 2], padding='same')(relu11_1)
pad12_1 = tf.pad(maxpool12_1, paddings=tf.constant(np.load('weights_front/channel_padding_10_Paddings')))
add12_1 = Add()([conv12_1, pad12_1])
relu12_1 = ReLU()(add12_1)

# Block_13
depthconv13_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_12_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_12_Bias')))(relu12_1)
conv13_1 = Conv2D(filters=96, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_13_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_13_Bias')))(depthconv13_1)
add13_1 = Add()([conv13_1, relu12_1])
relu13_1 = ReLU()(add13_1)

# Block_14
depthconv14_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_13_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_13_Bias')))(relu13_1)
conv14_1 = Conv2D(filters=96, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_14_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_14_Bias')))(depthconv14_1)
add14_1 = Add()([conv14_1, relu13_1])
relu14_1 = ReLU()(add14_1)

# Block_15
depthconv15_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_14_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_14_Bias')))(relu14_1)
conv15_1 = Conv2D(filters=96, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_15_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_15_Bias')))(depthconv15_1)
add15_1 = Add()([conv15_1, relu14_1])
relu15_1 = ReLU()(add15_1)

# Block_16
depthconv16_1 = DepthwiseConv2D(kernel_size=[3, 3], strides=[1, 1], padding="same", depth_multiplier=1, dilation_rate=[1, 1],
                 depthwise_initializer=Constant(np.load('weights_front/depthwise_conv2d_15_Kernel')),
                 bias_initializer=Constant(np.load('weights_front/depthwise_conv2d_15_Bias')))(relu15_1)
conv16_1 = Conv2D(filters=96, kernel_size=[1, 1], strides=[1, 1], padding="valid", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/conv2d_16_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/conv2d_16_Bias')))(depthconv16_1)
add16_1 = Add()([conv16_1, relu15_1])
relu16_1 = ReLU()(add16_1)

# Block_17
conv17_1 = Conv2D(filters=2, kernel_size=[1, 1], strides=[1, 1], padding="same", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/classificator_8_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/classificator_8_Bias')))(relu11_1)
reshape17_1 = tf.reshape(conv17_1, (1, 512, 1), name='classificators_1')

# Block_18
conv18_1 = Conv2D(filters=6, kernel_size=[1, 1], strides=[1, 1], padding="same", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/classificator_16_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/classificator_16_Bias')))(relu16_1)
reshape18_1 = tf.reshape(conv18_1, (1, 384, 1), name='classificators_2')

# Block_19
conv19_1 = Conv2D(filters=32, kernel_size=[1, 1], strides=[1, 1], padding="same", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/regressor_8_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/regressor_8_Bias')))(relu11_1)
reshape19_1 = tf.reshape(conv19_1, (1, 512, 16), name='regressors_1')

conv19_2 = Conv2D(filters=96, kernel_size=[1, 1], strides=[1, 1], padding="same", dilation_rate=[1, 1],
                 kernel_initializer=Constant(np.load('weights_front/regressor_16_Kernel').transpose(1,2,3,0)),
                 bias_initializer=Constant(np.load('weights_front/regressor_16_Bias')))(relu16_1)
reshape19_2 = tf.reshape(conv19_2, (1, 384, 16), name='regressors_2')

model = Model(inputs=inputs, outputs=[reshape17_1, reshape18_1, reshape19_1, reshape19_2])

model.summary()

tf.saved_model.save(model, 'saved_model_face_detection_front')
model.save('face_detection_front.h5')


# No Quantization - Input/Output=float32
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('face_detection_front_128x128_float32.tflite', 'wb') as w:
    w.write(tflite_model)
print("tflite convert complete! - face_detection_front_128x128_float32.tflite")


# Weight Quantization - Input/Output=float32
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
tflite_model = converter.convert()
with open('face_detection_front_128x128_weight_quant.tflite', 'wb') as w:
    w.write(tflite_model)
print("Weight Quantization complete! - face_detection_front_128x128_weight_quant.tflite")


def representative_dataset_gen():
  for data in raw_test_data.take(100):
    image = data['image'].numpy()
    image = tf.image.resize(image, (128, 128))
    image = image[np.newaxis,:,:,:]
    image = image - 127.5
    image = image * 0.007843
    yield [image]

raw_test_data, info = tfds.load(name="the300w_lp", with_info=True, split="train", data_dir="~/TFDS", download=False)


# Integer Quantization - Input/Output=float32
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset_gen
tflite_quant_model = converter.convert()
with open('face_detection_front_128x128_integer_quant.tflite', 'wb') as w:
    w.write(tflite_quant_model)
print("Integer Quantization complete! - face_detection_front_128x128_integer_quant.tflite")


# Full Integer Quantization - Input/Output=int8
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8
converter.representative_dataset = representative_dataset_gen
tflite_quant_model = converter.convert()
with open('face_detection_front_128x128_full_integer_quant.tflite', 'wb') as w:
    w.write(tflite_quant_model)
print("Full Integer Quantization complete! - face_detection_front_128x128_full_integer_quant.tflite")


# Float16 Quantization - Input/Output=float32
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
tflite_quant_model = converter.convert()
with open('face_detection_front_128x128_float16_quant.tflite', 'wb') as w:
    w.write(tflite_quant_model)
print("Float16 Quantization complete! - face_detection_front_128x128_float16_quant.tflite")


# EdgeTPU
import subprocess
result = subprocess.check_output(["edgetpu_compiler", "-s", "face_detection_front_128x128_full_integer_quant.tflite"])
print(result)
