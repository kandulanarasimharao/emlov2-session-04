import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from typing import List, Tuple

import gradio as gr
import hydra
import torch
import torchvision.transforms as transforms
from omegaconf import DictConfig
from PIL import Image

from src import utils

log = utils.get_pylogger(__name__)

cifar10_labels = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def demo(cfg: DictConfig) -> Tuple[dict, dict]:
    """Demo function.
    Args:
        cfg (DictConfig): Configuration composed by Hydra.

    Returns:
        Tuple[dict, dict]: Dict with metrics and dict with all instantiated objects.
    """

    assert cfg.ckpt_path

    log.info("Running Demo")

    log.info(f"Instantiating scripted model <{cfg.ckpt_path}>")
    model = torch.jit.load(cfg.ckpt_path)

    log.info(f"Loaded Model: {model}")

    def recognize_image(image: Image):
        if image is None:
            return None
        image = transforms.ToTensor()(image).unsqueeze(0)
        preds = model.forward_jit(image)
        preds = preds[0].tolist()
        # print({cifar10_labels[i]: preds[i] for i in range(10)})
        return {cifar10_labels[i]: preds[i] for i in range(10)}

    im = gr.Image(shape=(32, 32), type="pil")

    demo = gr.Interface(
        fn=recognize_image,
        inputs=im,
        outputs=[gr.Label(num_top_classes=10)],
    )

    demo.launch(share=True)


@hydra.main(version_base="1.2", config_path=root / "configs", config_name="demo_scripted.yaml")
def main(cfg: DictConfig) -> None:
    demo(cfg)


if __name__ == "__main__":
    main()
