from dataclasses import dataclass
import gradio as gr
from env import Kubin
from ui_blocks.options.options_diffusers import options_tab_diffusers
from ui_blocks.options.options_general import options_tab_general
from ui_blocks.options.options_gradio import options_tab_gradio
from ui_blocks.options.options_ui import options_tab_ui


def options_ui(kubin: Kubin):
    with gr.Row() as options_block:
        with gr.Column(scale=1, elem_classes="options-left"):
            with gr.Box():
                gr.HTML(
                    "General",
                    elem_id="options-general",
                    elem_classes=["options-select", "selected"],
                )
                gr.HTML(
                    "Gradio", elem_id="options-gradio", elem_classes="options-select"
                )
                gr.HTML("UI", elem_id="options-ui", elem_classes="options-select")
                gr.HTML(
                    "Diffusers",
                    elem_id="options-diffusers",
                    elem_classes="options-select",
                )

        with gr.Column(scale=5):
            options_tab_general(kubin)
            options_tab_gradio(kubin)
            options_tab_ui(kubin)
            options_tab_diffusers(kubin)

    with gr.Row():
        apply_changes = gr.Button(
            value="🆗 Apply changes",
            label="Apply changes",
            interactive=True,
        )

        save_changes = gr.Button(
            value="💾 Save applied changes",
            label="Save changes",
            interactive=True,
        )

        reset_changes = gr.Button(
            value="⏮️ Reset to default",
            label="Reset to default",
            interactive=True,
        )

    with gr.Row():
        options_info = gr.HTML("")

    def apply():
        requires_reload = kubin.params.apply_config_changes()
        if requires_reload:
            kubin.model.flush()
            kubin.with_pipeline()

    apply_changes.click(
        fn=apply,
        queue=False,
    ).then(fn=None, _js='(e) => kubin.notify.success("Changes applied")')

    save_changes.click(
        fn=lambda: kubin.params.save_user_config(), queue=False, show_progress=False
    ).then(fn=None, _js='(e) => kubin.notify.success("Config saved")')

    reset_changes.click(
        fn=lambda: kubin.params.reset_config(), queue=False, show_progress=False
    ).then(
        fn=lambda: "Default configuration will be restored upon restarting the app",
        _js='(e) => kubin.notify.success("Restored default config")',
        outputs=[options_info],
    )

    return options_block
