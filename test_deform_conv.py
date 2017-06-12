import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import numpy as np
import tensorflow as tf
import lib.deform_conv_op as deform_conv_op

with open("test.npz", 'rb') as f:
  arr = np.load(f)

# arr = np.zeros((8, 6, 4, 5))
with tf.Session() as sess: 
  with tf.device('/gpu:0'):
    a = tf.constant(arr, dtype=tf.float32)
    b = tf.constant(np.ones((21,2,2,2), dtype = np.float32))
    c = tf.constant(np.ones((8,8,2,2), dtype = np.float32))
    result = deform_conv_op.deform_conv_op(a, b, c, strides=[1, 1, 2, 2], rates=[1,1,1,1], padding="SAME", num_groups=3)
    sm = sess.run(result)
    d = tf.constant(np.ones((8,21,2,2), dtype = np.float32))
    grad = tf.gradients(result, [a, b, c])
    res = [sess.run(g) for g in grad]

print(res[0])
# print(sm)

