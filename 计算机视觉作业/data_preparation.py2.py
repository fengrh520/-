import mindspore as ms
from mindspore.dataset import Cifar10Dataset
from mindspore.dataset import vision, transforms
from download import download


def get_dataset(train_dataset_path, batch_size, usage, data_augmentation_config):
    image_trans = []
    if usage == "train":
        for aug_config in data_augmentation_config["train"]:
            if aug_config["name"] == "RandomCrop":
                image_trans.append(vision.RandomCrop(aug_config["size"], aug_config["padding"]))
            elif aug_config["name"] == "RandomHorizontalFlip":
                image_trans.append(vision.RandomHorizontalFlip(prob=aug_config["prob"]))
            elif aug_config["name"] == "Resize":
                image_trans.append(vision.Resize(aug_config["size"]))
            elif aug_config["name"] == "Rescale":
                image_trans.append(vision.Rescale(aug_config["scale"], aug_config["shift"]))
            elif aug_config["name"] == "Normalize":
                image_trans.append(vision.Normalize(aug_config["mean"], aug_config["std"]))
            elif aug_config["name"] == "HWC2CHW":
                image_trans.append(vision.HWC2CHW())
    elif usage == "test":
        for aug_config in data_augmentation_config["test"]:
            if aug_config["name"] == "Resize":
                image_trans.append(vision.Resize(aug_config["size"]))
            elif aug_config["name"] == "Rescale":
                image_trans.append(vision.Rescale(aug_config["scale"], aug_config["shift"]))
            elif aug_config["name"] == "Normalize":
                image_trans.append(vision.Normalize(aug_config["mean"], aug_config["std"]))
            elif aug_config["name"] == "HWC2CHW":
                image_trans.append(vision.HWC2CHW())

    label_trans = transforms.TypeCast(ms.int32)
    dataset = Cifar10Dataset(train_dataset_path, usage=usage, shuffle=True)
    dataset = dataset.map(image_trans, 'image')
    dataset = dataset.map(label_trans, 'label')
    dataset = dataset.batch(batch_size, drop_remainder=True)
    return dataset


def download_cifar10_dataset(url, save_path, kind="tar.gz", replace=True):
    download(url, save_path, kind=kind, replace=replace)