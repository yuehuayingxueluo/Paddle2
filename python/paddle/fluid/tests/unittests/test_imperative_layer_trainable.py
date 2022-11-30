# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np

import paddle.fluid as fluid
import paddle.fluid.dygraph as dygraph
from paddle.fluid.framework import _test_eager_guard
import paddle


class TestImperativeLayerTrainable(unittest.TestCase):
    def func_set_trainable(self):
        with fluid.dygraph.guard():
            label = np.random.uniform(-1, 1, [10, 10]).astype(np.float32)

            label = dygraph.to_variable(label)

            linear = paddle.nn.Linear(10, 10)
            y = linear(label)
            self.assertFalse(y.stop_gradient)

            linear.weight.trainable = False
            linear.bias.trainable = False

            self.assertFalse(linear.weight.trainable)
            self.assertTrue(linear.weight.stop_gradient)

            y = linear(label)
            self.assertTrue(y.stop_gradient)

            with self.assertRaises(ValueError):
                linear.weight.trainable = "1"

    def test_set_trainable(self):
        with _test_eager_guard():
            self.func_set_trainable()
        self.func_set_trainable()


if __name__ == '__main__':
    unittest.main()
