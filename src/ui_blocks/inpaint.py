import gradio as gr
from ui_blocks.shared.ui_shared import SharedUI


def inpaint_gallery_select(evt: gr.SelectData):
    return [evt.index, f"Selected image index: {evt.index}"]


# TODO: implement region of inpainting
def inpaint_ui(generate_fn, shared: SharedUI, tabs):
    selected_inpaint_image_index = gr.State(None)  # type: ignore
    augmentations = shared.create_ext_augment_blocks("inpaint")

    with gr.Row() as inpaint_block:
        with gr.Column(scale=2):
            with gr.Row():
                shared.input_inpaint_image.render()
                with gr.Column():
                    prompt = gr.Textbox("", placeholder="", label="Prompt")
                    negative_prompt = gr.Textbox(
                        "", placeholder="", label="Negative prompt"
                    )

            with gr.Accordion("Advanced params", open=True):
                with gr.Row():
                    inpainting_target = gr.Radio(
                        ["only mask", "all but mask"],
                        value="only mask",
                        label="Inpainting target",
                    )
                    inpainting_region = gr.Radio(
                        ["whole", "mask"],
                        value="whole",
                        label="Inpainting region",
                        visible=False,
                    )
                with gr.Row():
                    steps = gr.Slider(1, 200, 100, step=1, label="Steps")
                    guidance_scale = gr.Slider(
                        1, 30, 10, step=1, label="Guidance scale"
                    )
                with gr.Row():
                    batch_count = gr.Slider(1, 16, 4, step=1, label="Batch count")
                    batch_size = gr.Slider(1, 16, 1, step=1, label="Batch size")
                    # TODO: fix https://github.com/ai-forever/Kandinsky-2/issues/53
                with gr.Row():
                    width = gr.Slider(
                        shared.ui_params("image_width_min"),
                        shared.ui_params("image_width_max"),
                        shared.ui_params("image_width_default"),
                        step=shared.ui_params("image_width_step"),
                        label="Width",
                    )
                    height = gr.Slider(
                        shared.ui_params("image_height_min"),
                        shared.ui_params("image_height_max"),
                        shared.ui_params("image_height_default"),
                        step=shared.ui_params("image_height_step"),
                        label="Height",
                    )
                with gr.Row():
                    sampler = gr.Radio(
                        ["ddim_sampler", "p_sampler", "plms_sampler"],
                        value="p_sampler",
                        label="Sampler",
                    )
                    seed = gr.Number(-1, label="Seed", precision=0)
                with gr.Row():
                    prior_scale = gr.Slider(1, 100, 4, step=1, label="Prior scale")
                    prior_steps = gr.Slider(1, 100, 5, step=1, label="Prior steps")
                    negative_prior_prompt = gr.Textbox(
                        "", label="Negative prior prompt"
                    )

            augmentations["ui"]()

        with gr.Column(scale=1):
            generate_inpaint = gr.Button("Generate", variant="primary")
            inpaint_output = gr.Gallery(label="Generated Images").style(
                grid=2, preview=True
            )
            selected_image_info = gr.HTML(value="", elem_classes=["block-info"])
            inpaint_output.select(
                fn=inpaint_gallery_select,
                outputs=[selected_inpaint_image_index, selected_image_info],
                show_progress=False,
            )

            shared.create_base_send_targets(
                inpaint_output, selected_inpaint_image_index, tabs
            )
            shared.create_ext_send_targets(
                inpaint_output, selected_inpaint_image_index, tabs
            )

            def generate(
                image_mask,
                prompt,
                negative_prompt,
                inpainting_target,
                inpainting_region,
                steps,
                batch_count,
                batch_size,
                guidance_scale,
                w,
                h,
                sampler,
                prior_cf_scale,
                prior_steps,
                negative_prior_prompt,
                input_seed,
                *injections,
            ):
                params = {
                    "image_mask": image_mask,
                    "prompt": prompt,
                    "negative_decoder_prompt": negative_prompt,
                    "target": inpainting_target,
                    "region": inpainting_region,
                    "num_steps": steps,
                    "batch_count": batch_count,
                    "batch_size": batch_size,
                    "guidance_scale": guidance_scale,
                    "w": w,
                    "h": h,
                    "sampler": sampler,
                    "prior_cf_scale": prior_cf_scale,
                    "prior_steps": prior_steps,
                    "negative_prior_prompt": negative_prior_prompt,
                    "input_seed": input_seed,
                }

                params = augmentations["exec"](params, injections)
                return generate_fn(params)

        generate_inpaint.click(
            generate,
            inputs=[
                shared.input_inpaint_image,
                prompt,
                negative_prompt,
                inpainting_target,
                inpainting_region,
                steps,
                batch_count,
                batch_size,
                guidance_scale,
                width,
                height,
                sampler,
                prior_scale,
                prior_steps,
                negative_prior_prompt,
                seed,
            ]
            + augmentations["injections"],
            outputs=inpaint_output,
        )

    return inpaint_block
