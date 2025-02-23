from __future__ import print_function
from __future__ import division

import os
import numpy as np
import time
import skimage.io as skio
import argparse
import matplotlib.pyplot as plt
import demo

if __name__ == "__main__":
    plt.switch_backend("agg")
    parser = argparse.ArgumentParser()
    parser.add_argument("--im_path", type=str, help="path_to_image")
    cfg = parser.parse_args()

    assert os.path.exists(cfg.im_path)

    imid = cfg.im_path.split("/")[-1].split(".")[0]
    save_path = os.path.join("./images", f"{imid}_ncuts_result.png")

    ckpt_path = "./ckpt/exif_final/exif_final.ckpt"
    exif_demo = demo.Demo(ckpt_path=ckpt_path, use_gpu=0, quality=3.0, num_per_dim=30)

    print(f"Running image {cfg.im_path}")
    ms_st = time.time()
    im_path = cfg.im_path
    im1 = skio.imread(im_path)[:, :, :3].astype(np.float32)
    res = exif_demo.run(im1, use_ncuts=True, blue_high=True)
    print("MeanShift run time: %.3f" % (time.time() - ms_st))

    plt.subplots(figsize=(16, 8))
    plt.subplot(1, 3, 1)
    plt.title("Input Image")
    plt.imshow(im1.astype(np.uint8))
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Cluster w/ MeanShift")
    plt.axis("off")
    plt.imshow(res[0], cmap="jet", vmin=0.0, vmax=1.0)

    plt.subplot(1, 3, 3)
    plt.title("Segment with NCuts")
    plt.axis("off")
    plt.imshow(res[1], vmin=0.0, vmax=1.0)

    plt.savefig(save_path)
    print(f"Result saved {save_path}")
