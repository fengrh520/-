import mindspore
from mindspore import load_checkpoint, load_param_into_net
from model_definition import ShuffleNetV1


def test(data_path, batch_size, n_class, model_size, group):
    mindspore.set_context(mode=mindspore