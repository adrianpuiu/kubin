import argparse
from env import Kubin
from webui import gradio_ui
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='Run Kubin')
parser.add_argument('--from-config', type=str, default='') # unused 
parser.add_argument('--device', type=str, default='cuda')
parser.add_argument('--model-version', type=str, default='2.1')
parser.add_argument('--use-flash-attention', default=False, action='store_true')
parser.add_argument('--cache-dir', type=str, default='models')
parser.add_argument('--output-dir', type=str, default='output')
parser.add_argument('--task-type', type=str, default='text2img')
parser.add_argument('--share', type=str, default='none')
parser.add_argument('--server-name', type=str, default='127.0.0.1')
parser.add_argument('--server-port', type=int, default=7860)
parser.add_argument('--concurrency-count', type=int, default=2)
parser.add_argument('--debug', default=True, action='store_true')
parser.add_argument('--model-config', type=str, default='config.kd2') #  unused
parser.add_argument('--max-mix', type=int, default=2) # unused 
parser.add_argument('--extensions-path', type=str, default='extensions')
parser.add_argument('--enabled-extensions', type=str, default=None)
parser.add_argument('--disabled-extensions', type=str, default=None)
parser.add_argument('--skip-install', default=False, action='store_true')
parser.add_argument('--safe-mode', default=False, action='store_true')
parser.add_argument('--mock', default=False, action='store_true')
parser.add_argument('--pipeline', type=str, default='native') # unused 
parser.add_argument('--theme', type=str, default='default') 

args = parser.parse_args()
print(f'launching with: {vars(args)}')

kubin = Kubin(args)
kubin.with_utils()
kubin.with_extensions()

ui, resources = gradio_ui(kubin)
ui.queue(concurrency_count=kubin.options.concurrency_count, api_open=False).launch(
  show_api=False,
  debug=kubin.options.debug,
  show_error=True,
  share=kubin.options.share=='gradio',
  server_name=kubin.options.server_name,
  server_port=kubin.options.server_port,
  allowed_paths=[f'{Path(__file__).parent.parent.absolute()}/client'] + resources
)