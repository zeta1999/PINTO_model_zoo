### tensorflow==2.3.1

### https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/6.0/GA_6.0.1.5/local_repos/nv-tensorrt-repo-ubuntu1804-cuda10.1-trt6.0.1.5-ga-20190913_1-1_amd64.deb

# os="ubuntu1804"
# tag="cuda10.1-trt6.0.1.5-ga-20190913"
# sudo dpkg -i nv-tensorrt-repo-${os}-${tag}_1-1_amd64.deb
# sudo apt-key add /var/nv-tensorrt-repo-${tag}/7fa2af80.pub

# sudo apt-get update
# sudo apt-get install tensorrt

# sudo apt-get install python3-libnvinfer-dev
# python3-libnvinfer
# sudo apt-get install uff-converter-tf
# sudo apt-get install onnx-graphsurgeon

import tensorflow as tf
import numpy as np
import time

height_256 = 256
width_256  = 256

height_320 = 320
width_320  = 320


def input_fn_256():
    input_shapes = [1, height_256, width_256, 3]
    yield [np.zeros(input_shapes).astype(np.float32)]

def input_fn_320():
    input_shapes = [1, height_320, width_320, 3]
    yield [np.zeros(input_shapes).astype(np.float32)]


params = tf.experimental.tensorrt.ConversionParams(precision_mode='FP32', maximum_cached_engines=1000)
converter = tf.experimental.tensorrt.Converter(input_saved_model_dir='saved_model_{}x{}'.format(height_256, width_256), conversion_params=params)
converter.convert()
converter.build(input_fn=input_fn_256)
converter.save('tensorrt_saved_model_{}x{}_float32'.format(height_256, width_256))

params = tf.experimental.tensorrt.ConversionParams(precision_mode='FP16', maximum_cached_engines=1000)
converter = tf.experimental.tensorrt.Converter(input_saved_model_dir='saved_model_{}x{}'.format(height_256, width_256), conversion_params=params)
converter.convert()
converter.build(input_fn=input_fn_256)
converter.save('tensorrt_saved_model_{}x{}_float16'.format(height_256, width_256))



params = tf.experimental.tensorrt.ConversionParams(precision_mode='FP32', maximum_cached_engines=1000)
converter = tf.experimental.tensorrt.Converter(input_saved_model_dir='saved_model_{}x{}'.format(height_320, width_320), conversion_params=params)
converter.convert()
converter.build(input_fn=input_fn_320)
converter.save('tensorrt_saved_model_{}x{}_float32'.format(height_320, width_320))

params = tf.experimental.tensorrt.ConversionParams(precision_mode='FP16', maximum_cached_engines=1000)
converter = tf.experimental.tensorrt.Converter(input_saved_model_dir='saved_model_{}x{}'.format(height_320, width_320), conversion_params=params)
converter.convert()
converter.build(input_fn=input_fn_320)
converter.save('tensorrt_saved_model_{}x{}_float16'.format(height_320, width_320))



model = tf.saved_model.load('tensorrt_saved_model_{}x{}_float32'.format(height_320, width_320), tags=[tf.saved_model.SERVING])
infer = model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
infer.inputs[0].shape
x = np.random.uniform(size=(1,height_320, width_320,3)).astype(np.float32)
start = time.perf_counter()
infer(tf.convert_to_tensor(x))
end = time.perf_counter()
print('@@@@@@@@@@@@@@ First Inference')
print('elapsed time:', end - start)
start = time.perf_counter()
infer(tf.convert_to_tensor(x))
end = time.perf_counter()
print('@@@@@@@@@@@@@@ Second Inference')
print('elapsed time:', end - start)
