import gradio as gr
import os
from train_modules.train_tools import relative_path_app_warning, relative_path_extension_warning, save_config_to_path, load_config_from_path
from train_modules.train_unclip import default_unclip_config_path, add_default_values, start_unclip_training

def train_unclip_ui(kubin, tabs):
  default_config_from_path = load_config_from_path(default_unclip_config_path)
  default_config_from_path = add_default_values(kubin.options.cache_dir, default_config_from_path)

  with gr.Row() as train_unclip_block:
    current_config = gr.State(default_config_from_path)

    with gr.Column(scale=3):
      with gr.Accordion('General params', open=True):
        with gr.Row():
          params_path = gr.Textbox(value=default_config_from_path['params_path'], label='Params path', interactive=True, info=relative_path_app_warning) # type: ignore
          clip_name = gr.Textbox(value=default_config_from_path['clip_name'], label='Clip Name', interactive=True) # type: ignore
          save_path = gr.Textbox(value=default_config_from_path['save_path'], label='Save path', interactive=True, info=relative_path_extension_warning) # type: ignore
          save_name = gr.Textbox(value=default_config_from_path['save_name'], label='Save name', interactive=True) # type: ignore
        with gr.Row():
          with gr.Column():
            num_epochs = gr.Number(value=default_config_from_path['num_epochs'], label='Number of epochs', interactive=True) # type: ignore
            save_every = gr.Number(value=default_config_from_path['save_every'], label='Save every', interactive=True) # type: ignore
          with gr.Column():
            device = gr.Textbox(value=default_config_from_path['device'], label='Device', interactive=True) # type: ignore
            num_workers = gr.Number(value=default_config_from_path['data']['train']['num_workers'], label='Number of workers', info='Set to 0 if Windows', interactive=True) # type: ignore
          with gr.Column():
            inpainting = gr.Checkbox(value=default_config_from_path['inpainting'], label='Inpainting', interactive=True) # type: ignore
            shuffle = gr.Checkbox(value=default_config_from_path['data']['train']['shuffle'], label='Shuffle', interactive=True) # type: ignore
            drop_first_layer = gr.Checkbox(value=default_config_from_path['drop_first_layer'], label='Drop first layer', interactive=True)  # type: ignore
            freeze_resblocks = gr.Checkbox(value=default_config_from_path['freeze']['freeze_resblocks'], label='Freeze Residual Blocks', interactive=True)  # type: ignore
            freeze_attention = gr.Checkbox(value=default_config_from_path['freeze']['freeze_attention'], label='Freeze Attention', interactive=True)  # type: ignore
          
        with gr.Row():
          with gr.Column():
            with gr.Row():
              df_path = gr.Textbox(value=default_config_from_path['data']['train']['df_path'], label='Dataset path', interactive=True, info=relative_path_extension_warning) # type: ignore
              open_tools = gr.Button('Dataset preparation').style(size='sm', full_width=False)
              open_tools.click(lambda: gr.Tabs.update(selected='training-tools'), outputs=tabs)
          with gr.Column():
            image_size = gr.Textbox(value=default_config_from_path['data']['train']['image_size'], label='Image Size', interactive=True) # type: ignore
            tokenizer_name = gr.Textbox(value=default_config_from_path['data']['train']['tokenizer_name'], label='Tokenizer Name', interactive=True) # type: ignore
          with gr.Column():
            clip_image_size = gr.Number(value=default_config_from_path['data']['train']['clip_image_size'], label='Clip image size', interactive=True) # type: ignore
            drop_text_prob = gr.Number(value=default_config_from_path['data']['train']['drop_text_prob'], label='Dropout text probability', interactive=True) # type: ignore
        with gr.Row():
          drop_image_prob = gr.Number(value=default_config_from_path['data']['train']['drop_image_prob'], label='Dropout image probability', interactive=True) # type: ignore
          seq_len = gr.Number(value=default_config_from_path['data']['train']['seq_len'], label='Sequence Length', interactive=True) # type: ignore
          batch_size = gr.Number(value=default_config_from_path['data']['train']['batch_size'], label='Batch size', interactive=True) # type: ignore

      with gr.Accordion('Optimizer params', open=True):
        with gr.Row():
          with gr.Column(scale=2):
            with gr.Row():
              optimizer_name = gr.Textbox(value=default_config_from_path['optim_params']['name'], label='Optimizer name', interactive=True) # type: ignore
              lr = gr.Number(value=default_config_from_path['optim_params']['params']['lr'], label='Learning rate', interactive=True) # type: ignore
              weight_decay = gr.Number(value=default_config_from_path['optim_params']['params']['weight_decay'], label='Weight decay', interactive=True) # type: ignore
          with gr.Column(scale=1):
            scale_parameter = gr.Checkbox(value=default_config_from_path['optim_params']['params']['scale_parameter'], label='Scale parameter', interactive=True) # type: ignore
            relative_step = gr.Checkbox(value=default_config_from_path['optim_params']['params']['relative_step'], label='Relative step', interactive=True) # type: ignore

      with gr.Accordion('Image encoder params', open=True):
        with gr.Row():
          scale = gr.Number(value=default_config_from_path['image_enc_params']['scale'], label='Scale', interactive=True) # type: ignore
          ckpt_path = gr.Textbox(value=default_config_from_path['image_enc_params']['ckpt_path'], label='Checkpoint Path', interactive=True) # type: ignore
          embed_dim = gr.Number(value=default_config_from_path['image_enc_params']['params']['embed_dim'], label='Embedding Dimension', interactive=True) # type: ignore
          n_embed = gr.Number(value=default_config_from_path['image_enc_params']['params']['n_embed'], label='Number of Embeddings', interactive=True) # type: ignore
        with gr.Row():
          double_z = gr.Checkbox(value=default_config_from_path['image_enc_params']['params']['ddconfig']['double_z'], label='Double Z', interactive=True) # type: ignore
          z_channels = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['z_channels'], label='Z Channels', interactive=True) # type: ignore
          resolution = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['resolution'], label='Resolution', interactive=True) # type: ignore
          in_channels = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['in_channels'], label='Input Channels', interactive=True) # type: ignore
          out_ch = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['out_ch'], label='Output Channels', interactive=True) # type: ignore
          ch = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['ch'], label='Channels', interactive=True) # type: ignore
          ch_mult = gr.Textbox(value=default_config_from_path['image_enc_params']['params']['ddconfig']['ch_mult'], label=' Channel Multiplier', interactive=True) # type: ignore
        with gr.Row():
          num_res_blocks = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['num_res_blocks'], label='Number of Residual Blocks', interactive=True) # type: ignore
          attn_resolutions = gr.Textbox(value=default_config_from_path['image_enc_params']['params']['ddconfig']['attn_resolutions'], label='Attention Resolutions', interactive=True) # type: ignore
          dropout = gr.Number(value=default_config_from_path['image_enc_params']['params']['ddconfig']['dropout'], label='Dropout', interactive=True) # type: ignore
      
      with gr.Accordion('Text encoder params', open=True):
        with gr.Row():
          model_path = gr.Textbox(value=default_config_from_path['text_enc_params']['model_path'], label='Model Path', interactive=True) # type: ignore
          model_name = gr.Textbox(value=default_config_from_path['text_enc_params']['model_name'], label='Model Name', interactive=True) # type: ignore
          in_features = gr.Number(value=default_config_from_path['text_enc_params']['in_features'], label='Input Features', interactive=True) # type: ignore
          out_features = gr.Number(value=default_config_from_path['text_enc_params']['out_features'], label='Output Features', interactive=True) # type: ignore
        
      with gr.Accordion('Miscellaneous', open=True):
        with gr.Row():
          config_path = gr.Textbox('train/train_unclip_config.yaml', label='Config path', info=relative_path_extension_warning)
          load_config = gr.Button('Load parameters from file').style(size='sm', full_width=False)
          save_config = gr.Button('Save parameters to file').style(size='sm', full_width=False)
          reset_config = gr.Button('Reset parameters to default values').style(size='sm', full_width=False)
     
      config_params = {
        current_config,
        params_path,
        drop_first_layer,
        clip_name,
        num_epochs,
        save_every,
        save_name,
        save_path,
        device,
        num_workers,
        inpainting,
        shuffle,
        freeze_resblocks,
        freeze_attention,
        df_path,
        image_size,
        tokenizer_name,
        clip_image_size,
        drop_text_prob,
        drop_image_prob,
        seq_len,
        batch_size,
        optimizer_name,
        lr,
        weight_decay,
        scale_parameter,
        relative_step,
        scale,
        ckpt_path,
        embed_dim,
        n_embed,
        double_z,
        z_channels,
        resolution,
        in_channels,
        out_ch,
        ch,
        ch_mult,
        num_res_blocks,
        attn_resolutions,
        dropout,
        model_path,
        model_name,
        in_features,
        out_features
      }
      
      def insert_values_to_ui(current_config):
        return {
          params_path: current_config['params_path'],
          drop_first_layer: current_config['drop_first_layer'],
          clip_name: current_config['clip_name'],
          num_epochs: current_config['num_epochs'],
          save_every: current_config['save_every'],
          save_name: current_config['save_name'],
          save_path: current_config['save_path'],
          device: current_config['device'],
          num_workers: current_config['data']['train']['num_workers'],
          inpainting: current_config['inpainting'],
          shuffle: current_config['data']['train']['shuffle'],
          freeze_resblocks: current_config['freeze']['freeze_resblocks'],
          freeze_attention: current_config['freeze']['freeze_attention'],
          df_path: current_config['data']['train']['df_path'],
          image_size: current_config['data']['train']['image_size'],
          tokenizer_name: current_config['data']['train']['tokenizer_name'],
          clip_image_size: current_config['data']['train']['clip_image_size'],
          drop_text_prob: current_config['data']['train']['drop_text_prob'],
          drop_image_prob: current_config['data']['train']['drop_image_prob'],
          seq_len: current_config['data']['train']['seq_len'],
          batch_size: current_config['data']['train']['batch_size'],
          optimizer_name: current_config['optim_params']['name'],
          lr: current_config['optim_params']['params']['lr'],
          weight_decay: current_config['optim_params']['params']['weight_decay'],
          scale_parameter: current_config['optim_params']['params']['scale_parameter'],
          relative_step: current_config['optim_params']['params']['relative_step'],
          scale: current_config['image_enc_params']['scale'],
          ckpt_path: current_config['image_enc_params']['ckpt_path'],
          embed_dim: current_config['image_enc_params']['params']['embed_dim'],
          n_embed: current_config['image_enc_params']['params']['n_embed'],
          double_z: current_config['image_enc_params']['params']['ddconfig']['double_z'],
          z_channels: current_config['image_enc_params']['params']['ddconfig']['z_channels'],
          resolution: current_config['image_enc_params']['params']['ddconfig']['resolution'],
          in_channels: current_config['image_enc_params']['params']['ddconfig']['in_channels'],
          out_ch: current_config['image_enc_params']['params']['ddconfig']['out_ch'],
          ch: current_config['image_enc_params']['params']['ddconfig']['ch'],
          ch_mult: current_config['image_enc_params']['params']['ddconfig']['ch_mult'],
          num_res_blocks: current_config['image_enc_params']['params']['ddconfig']['num_res_blocks'],
          attn_resolutions: current_config['image_enc_params']['params']['ddconfig']['attn_resolutions'],
          dropout: current_config['image_enc_params']['params']['ddconfig']['dropout'],
          model_path: current_config['text_enc_params']['model_path'],
          model_name: current_config['text_enc_params']['model_name'],
          in_features: current_config['text_enc_params']['in_features'],
          out_features: current_config['text_enc_params']['out_features'],
        }

      def update_config_from_ui(params):
        updated_config = default_config_from_path.copy()

        updated_config['params_path'] = params[params_path] # type: ignore
        updated_config['drop_first_layer'] = params[drop_first_layer] # type: ignore
        updated_config['clip_name'] = params[clip_name] # type: ignore
        updated_config['num_epochs'] = int(params[num_epochs]) # type: ignore
        updated_config['save_every'] = int(params[save_every]) # type: ignore
        updated_config['save_name'] = params[save_name] # type: ignore
        updated_config['save_path'] = params[save_path] # type: ignore
        updated_config['device'] = params[device] # type: ignore
        updated_config['data']['train']['num_workers'] = int(params[num_workers]) # type: ignore
        updated_config['inpainting'] = params[inpainting] # type: ignore
        updated_config['data']['train']['shuffle'] = params[shuffle] # type: ignore
        updated_config['freeze']['freeze_resblocks'] = params[freeze_resblocks] # type: ignore
        updated_config['freeze']['freeze_attention'] = params[freeze_attention] # type: ignore
        updated_config['data']['train']['df_path'] = params[df_path] # type: ignore
        updated_config['data']['train']['image_size'] = int(params[image_size]) # type: ignore
        updated_config['data']['train']['tokenizer_name'] = params[tokenizer_name]  # type: ignore
        updated_config['data']['train']['clip_image_size'] = int(params[clip_image_size]) # type: ignore
        updated_config['data']['train']['drop_text_prob'] = params[drop_text_prob] # type: ignore
        updated_config['data']['train']['drop_image_prob'] = params[drop_image_prob] # type: ignore
        updated_config['data']['train']['seq_len'] = int(params[seq_len]) # type: ignore
        updated_config['data']['train']['batch_size'] = int(params[batch_size]) # type: ignore
        updated_config['optim_params']['name'] = params[optimizer_name] # type: ignore
        updated_config['optim_params']['params']['lr'] = params[lr] # type: ignore
        updated_config['optim_params']['params']['weight_decay'] = int(params[weight_decay]) # type: ignore
        updated_config['optim_params']['params']['scale_parameter'] = params[scale_parameter] # type: ignore
        updated_config['optim_params']['params']['relative_step'] = params[relative_step] # type: ignore
        updated_config['image_enc_params']['scale'] = int(params[scale]) # type: ignore
        updated_config['image_enc_params']['ckpt_path'] = params[ckpt_path]  # type: ignore
        updated_config['image_enc_params']['params']['embed_dim'] = int(params[embed_dim]) # type: ignore
        updated_config['image_enc_params']['params']['n_embed'] = int(params[n_embed]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['double_z'] = params[double_z] # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['z_channels'] = int(params[z_channels]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['resolution'] = int(params[resolution]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['in_channels'] = int(params[in_channels]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['out_ch'] = int(params[out_ch]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['ch'] = int(params[ch]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['ch_mult'] = params[ch_mult] # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['num_res_blocks'] = int(params[num_res_blocks]) # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['attn_resolutions'] = params[attn_resolutions] # type: ignore
        updated_config['image_enc_params']['params']['ddconfig']['dropout'] = params[dropout] # type: ignore
        updated_config['text_enc_params']['model_path'] = params[model_path] # type: ignore
        updated_config['text_enc_params']['model_name'] = params[model_name] # type: ignore
        updated_config['text_enc_params']['in_features'] = int(params[in_features]) # type: ignore
        updated_config['text_enc_params']['out_features'] = int(params[out_features]) # type: ignore
        
        return updated_config
      
      def load_config_values(root_path, path, current_config):
        path = path if os.path.isabs(path) else os.path.join(root_path, path)
        return load_config_values_from_path(path, current_config)
      
      def load_config_values_from_path(path, current_config):
        if os.path.exists(path):
          config_from_path = load_config_from_path(path)
          return config_from_path, False
        else:
          print('path not found')
          return current_config, True

      def append_recommended_values(current_config):
        current_config = add_default_values(kubin.options.cache_dir, current_config)
        return current_config

      def save_config_values(root_path, path, current_config):
        path = path if os.path.isabs(path) else os.path.join(root_path, path)
        if os.path.exists(path):
          print('existing unclip config file found, overwriting')

        save_config_to_path(current_config, path)
        return False

      dir_root = gr.State(kubin.root)
      config_error = gr.Checkbox(False, visible=False)
      
      load_config.click(
        fn=load_config_values, inputs=[dir_root, config_path, current_config], outputs=[current_config, config_error], queue=False).then(
        fn=insert_values_to_ui, inputs=current_config, show_progress=False, outputs=config_params).then( # type: ignore
        fn=None, inputs=[config_error], outputs=[config_error], show_progress=False, _js='(e) => !e ? kubin.notify.success("Parameters loaded from file") : kubin.notify.error("Error loading config")')
              
      save_config.click(fn=update_config_from_ui, inputs=config_params, outputs=[current_config], queue=False).then( # type: ignore
        fn=save_config_values, inputs=[dir_root, config_path, current_config], outputs=[config_error], queue=False).then( # type: ignore
        fn=None, inputs=[config_error], outputs=[config_error], show_progress=False, _js='(e) => !e ? kubin.notify.success("Parameters saved to file") : kubin.notify.error("Error loading config")')
      
      reset_config.click(
        fn=load_config_values_from_path, inputs=[gr.State(default_unclip_config_path), current_config], outputs=[current_config, config_error], queue=False).then(
        fn=append_recommended_values, inputs=[current_config], outputs=[current_config], queue=False).then(
        fn=insert_values_to_ui, inputs=current_config, outputs=config_params, queue=False).then( # type: ignore
        fn=None, inputs=[config_error], outputs=[config_error], show_progress=False, _js='() => kubin.notify.success("Parameters were reset to default values")')

    with gr.Column(scale=1):
      ready_to_train = gr.State(False)
      start_training = gr.Button('Start training', variant='primary')
      unclip_training_info = gr.HTML('Training not started')

      def check_training_params(config):
        return True, ''
  
      def launch_training(success, root_path, training_config):
        if not success:
          return
        
        path = training_config['save_path']
        path = path if os.path.isabs(path) else os.path.join(root_path, path)

        if not os.path.exists(path):
          print(f'creating output path {path}')
          os.mkdir(path)

        start_unclip_training(kubin, training_config)
        return 'Training finished'

      training_config = gr.State(default_config_from_path)
      start_training.click(
        fn=update_config_from_ui, inputs=config_params, outputs=[training_config], queue=False).then( 
        fn=check_training_params, inputs=[training_config], outputs=[ready_to_train, unclip_training_info], queue=False, show_progress=False).then(
        fn=launch_training, inputs=[ready_to_train, dir_root, training_config], outputs=[unclip_training_info])

  return train_unclip_block