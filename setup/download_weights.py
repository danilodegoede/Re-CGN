"""Downloads pretrained model weights for the experiments in this repo."""
import os
from os.path import join, exists, isdir
from glob import glob
import sys
import shutil
import subprocess
import tarfile
import zipfile

import repackage
repackage.up()

from experiments.experiment_utils import set_env, REPO_PATH
set_env()


def check_existing_weights(root_folder):
    weights = glob(join(root_folder, "*.pth"))
    weights = [os.path.basename(x) for x in weights]
    check_weights = {"biggan256.pth", "cgn.pth", "u2net.pth"}

    return check_weights.issubset(weights)


if __name__ == "__main__":
    check = check_existing_weights(
        root_folder=join(REPO_PATH, "cgn_framework/imagenet/weights"),
    )
    if not check:
        subprocess.call("bash scripts/download_weights.sh", shell=True)
    else:
        print("Weights already downloaded.")
    
    # download ResNet50 trained from scratch weights
    # references:
    # 1. https://github.com/clovaai/CutMix-PyTorch#experimental-results-and-pretrained-models
    # 2. https://github.com/hendrycks/natural-adv-examples/issues/9
    path = join(
        REPO_PATH,
        "cgn_framework/imagenet/weights/resnet50_from_scratch_model_best.pth.tar",
    )
    if not exists(path):
        subprocess.call("bash scripts/download_resnet50_trained_from_scratch.sh", shell=True)
    else:
        print("ResNet50 trained from scratch weights already downloaded.")
    
    # download invariant classifier trained on IN-mini (trained by us)
    path = join(
        REPO_PATH,
        "cgn_framework/imagenet/weights/classifier_on_in-mini_model_best.pth",
    )
    if not exists(path):
        subprocess.call("gdown https://drive.google.com/uc?id=19D7_t3uzA_OlV4fA21Jm6bcB8GJMzPnK", shell=True)
        subprocess.call("mv model_best.pth {}".format(path), shell=True)
    else:
        print("Invariant classifier trained on IN-mini weights already downloaded.")