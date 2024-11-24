import time
import mindspore
import numpy as np
from mindspore import Tensor, nn
from mindspore.train import ModelCheckpoint, CheckpointConfig, TimeMonitor, LossMonitor, Model, Top1CategoricalAccuracy, Top5CategoricalAccuracy
from model_definition import ShuffleNetV1


def train(data_path, batch_size, n_class, model_size, group, config):
    mindspore.set_context(mode=mindspore.PYNATIVE_MODE, device_target="GPU")
    net = ShuffleNetV1(model_size=model_size, n_class=n_class)
    loss = nn.CrossEntropyLoss(weight=None, reduction='mean', label_smoothing=0.1)
    min_lr = config["min_lr"]
    base_lr = config["base_lr"]
    lr_scheduler = mindspore.nn.cosine_decay_lr(min_lr,
                                                base_lr,
                                                config["batches_per_epoch"] * config["warmup_epochs"],
                                                config["batches_per_epoch"],
                                                decay_epoch=config["decay_epoch"])
    lr = Tensor(lr_scheduler[-1])
    optimizer = nn.Momentum(params=net.trainable_params(), learning_rate=lr, momentum=0.9, weight_decay=config["weight_decay"], loss_scale=1024)
    loss_scale_manager = ms.amp.FixedLossScaleManager(1024, drop_overflow_update=False)
    model = Model(net, loss_fn=loss, optimizer=optimizer, amp_level="O3", loss_scale_manager=loss_scale_manager)
    callback = [TimeMonitor(), LossMonitor()]
    save_ckpt_path = config["save_ckpt_path"]
    config_ckpt = CheckpointConfig(save_checkpoint_steps=config["save_checkpoint_steps"], keep_checkpoint_max=config["keep_checkpoint_max"])
    ckpt_callback = ModelCheckpoint("shufflenetv1", directory=save_ckpt_path, config=config_ckpt)
    callback += [ckpt_callback]

    print("============== Starting Training ==============")
    start_time = time.time()
    dataset = get_dataset(data_path, batch_size, "train", config["data_augmentation_config"])
    model.train(config["epochs"], dataset, callbacks=callback)
    use_time = time.time() - start_time
    hour = str(int(use_time // 60 // 60))
    minute = str(int(use_time // 60 % 60))
    second = str(int(use_time % 60))
    print("total time:" + hour + "h " + minute + "m " + second + "s")
    print("============== Train Success ==============")