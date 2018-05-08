import numpy as np
# from sklearn import datasets, svm, metrics
import tensorflow as tf
import datetime
from tensorflow.examples.tutorials.mnist import input_data

from PIL import Image

mnist = input_data.read_data_sets('./mnist', one_hot=True)

# classifier = svm.SVC(gamma=0.001)


class Number_Recongnizer:
    log = '/home/eeb02/PycharmProjects/number_recognizer/number_recognizer/my_model/my_model.ckpt'
    batch_size = 500

    def __init__(self):
        self.build_networks()

    def train(self):
        init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.session.run(init_op)
        self.load()
        for i in range(20000):
            b_x, b_y = mnist.train.next_batch(self.batch_size)
            b_x = b_x * 2 - 1
            _ = self.session.run(self.train_op, {self.x: b_x, self.y_: b_y, self.dropout_rate: 0.5})
            if i % 500 == 0:
                accuracy_print, sumery = self.session.run([self.accuracy, self.merged], {self.x: b_x, self.y_: b_y, self.dropout_rate: 1})
                print(accuracy_print)
                self.writer.add_summary(sumery, i)
        # self.saver.save(self.session, self.log)
        test_x, test_y = mnist.test.next_batch(2000)
        print('test accuracy = {}', format(self.session.run(self.accuracy, {self.x: test_x, self.y_: test_y, self.dropout_rate: 1})))

    def build_networks(self):

        self.x = tf.placeholder(tf.float32, [None, 784])
        self.y_ = tf.placeholder(tf.float32, [None, 10])
        self.dropout_rate = tf.placeholder(tf.float32)
        # y =[]
        #
        # for d in ['/device:GPU:0', '/device:GPU:1']:
        #     with tf.device(d):
        self.x_flat = tf.reshape(self.x, [-1, 28, 28, 1])
        # self.x_flat = tf.map_fn(lambda x:tf.random_crop(x, [28, 28, 1]), self.x_flat)
        # self.x_flat = tf.map_fn(tf.image.random_flip_left_right, self.x_flat)
        # self.x_flat = tf.map_fn(tf.image.random_flip_up_down, self.x_flat)
        # self.x_flat = tf.map_fn(lambda x:tf.contrib.image.rotate(x, tf.random_uniform([], -1.5, 1.5)), self.x_flat)
        # self.x_flat = tf.image.resize_images(self.x_flat, [20, 20])
        # self.x_flat = tf.image.pad_to_bounding_box(self.x_flat, tf.random_uniform([], minval=0, maxval=7, dtype=tf.int32),
        #                              tf.random_uniform([], minval=0, maxval=7, dtype=tf.int32), 28, 28)
        # self.x_flat = tf.map_fn(lambda x:tf.image.random_brightness(x,max_delta=63), self.x_flat)
        # self.x_flat = tf.map_fn(lambda x:tf.image.random_contrast(x,lower=0.2, upper=1.8), self.x_flat)
        # self.x_flat = tf.map_fn(tf.image.per_image_standardization, self.x_flat)
        self.cnn_1 = tf.layers.conv2d(self.x_flat, 16, 5, 1, 'same', activation=tf.nn.relu)
        self.pool_1 = tf.layers.max_pooling2d(self.cnn_1, 2, 2)  # 14, 14, 16
        self.cnn_2 = tf.layers.conv2d(self.pool_1, 32, 5, 1, 'same', activation=tf.nn.relu)
        self.pool_2 = tf.layers.max_pooling2d(self.cnn_2, 2, 2)  # 7, 7, 32
        self.cnn_3 = tf.layers.conv2d(self.pool_2, 64, 5, 1, 'same', activation=tf.nn.relu)
        self.cnn_3_flat = tf.reshape(self.cnn_3, [-1, 7 * 7 * 64])
        self.fc1 = tf.layers.dense(self.cnn_3_flat, 1024, activation=tf.nn.relu)
        self.dropout = tf.layers.dropout(self.fc1, self.dropout_rate)
        self.y = tf.layers.dense(self.dropout, 10)

        self.loss = tf.losses.softmax_cross_entropy(onehot_labels=self.y_, logits=self.y)
        self.train_op = tf.train.AdamOptimizer(0.00001).minimize(self.loss)
        self.accuracy = tf.metrics.accuracy(labels=tf.argmax(self.y_, 1), predictions=tf.argmax(self.y, 1))[1]

        self.predict = tf.argmax(self.y, 1)

        config = tf.ConfigProto(log_device_placement=True)
        config.gpu_options.per_process_gpu_memory_fraction = 1.0
        config.gpu_options.allow_growth = True
        self.session = tf.Session(config=config)

        tf.summary.scalar('loss', self.loss)
        self.merged = tf.summary.merge_all()
        logdir = "tensorboard/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"
        self.writer = tf.summary.FileWriter(logdir, self.session.graph)

        self.saver = tf.train.Saver()
        print("network builded")

    def test(self, data):
        data = np.reshape(data, [1, -1])
        data = data / 8.0 - 1.0
        # print(data)
        result = self.session.run(self.predict, {self.x: data, self.dropout_rate: 1})
        return result

    def load(self):
        self.saver.restore(self.session, self.log)


def main():
    number_recognizer = Number_Recongnizer()
    number_recognizer.train()
    # number_recognizer.load()
    # data, _ = mnist.test.next_batch(1)
    # print(data)
    # plt.imshow(np.reshape(data[0], (28, 28)), cmap='gray')
    # plt.draw()
    # plt.pause(5)

    # result = number_recognizer.test(data)
    # print(result)


if __name__ == "__main__":
    # try:
        main()
    # except Exception as ex:
    #     print(ex)
