import sys
import gradio as gr
import torch
import psutil
import platform
from kandinsky2 import CONFIG_2_1
from env import Kubin
from utils.yaml import flatten_yaml
from .settings_options import options_ui
from .settings_ckpt import ckpt_selector


def in_mb(bytes: float):
    return round(bytes / (1024**2))


def update_info():
    print("scanning system information")
    torch_version = torch.__version__
    cuda_version = torch.version.cuda

    if torch.cuda.is_available():
        torch_free, torch_total = torch.cuda.mem_get_info()
    else:
        torch_free, torch_total = 0, 0

    xformers_info = ""
    try:
        import xformers

        xformers_info = f"xformers: {xformers.__version__}\n"
    except:
        pass

    diffusers_info = ""
    try:
        import diffusers

        diffusers_info = f"diffusers: {diffusers.__version__}\n"
    except:
        pass

    transformers_info = ""
    try:
        import transformers

        transformers_info = f"transformers: {transformers.__version__}\n"
    except:
        pass

    vmem = psutil.virtual_memory()
    ram_total = vmem.total
    ram_available = vmem.available

    torch_total_mb = in_mb(torch_total)
    torch_free_mb = in_mb(torch_free)
    ram_total_mb = in_mb(ram_total)
    ram_available_mb = in_mb(ram_available)

    return (
        f"python: {sys.version}\n"
        f"torch: {torch_version}\n"
        f"CUDA: {cuda_version}\n"
        f"processor: {platform.processor()}\n"
        f"RAM (total): {ram_total_mb}\n"
        f"RAM (free): {ram_available_mb}\n"
        f"VRAM (total): {torch_total_mb}\n"
        f"VRAM (free): {torch_free_mb}\n"
        f"gradio: {gr.__version__}\n"
        f"{xformers_info}"
        f"{diffusers_info}"
        f"{transformers_info}"
    )


def settings_ui(kubin: Kubin, start_fn, ui):
    model_config = flatten_yaml(CONFIG_2_1)

    with gr.Column() as settings_block:
        with gr.TabItem("Options"):
            options_ui(kubin, start_fn, ui)

        with gr.TabItem("Checkpoints"):
            ckpt_selector(kubin)

        with gr.TabItem("System"):
            with gr.Row():
                system_info = gr.Textbox(
                    update_info,
                    lines=10,
                    label="System info",
                    interactive=False,
                    show_copy_button=True,
                )

                textbox_log = gr.Textbox(
                    label="System log",
                    lines=10,
                    interactive=False,
                    show_copy_button=True,
                )

            with gr.Row():
                update_btn = gr.Button(value="Update system info", scale=0, size="sm")
                update_btn.click(update_info, outputs=system_info)

                unload_model = gr.Button(value="Free memory", scale=0, size="sm")
                unload_model.click(lambda: kubin.model.flush(), queue=False).then(
                    fn=None, _js='_ => kubin.notify.success("Model unloaded")'
                )

            # with gr.Accordion("Model params", open=False):
            #     values = []
            #     for key in model_config:
            #         value = gr.Textbox(label=str(key), value=model_config[key])
            #         values.append(value)

    return settings_block
