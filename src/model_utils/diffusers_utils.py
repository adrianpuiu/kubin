from typing import Any
from diffusers import (
    DDIMInverseScheduler,
    DDIMScheduler,
    DDPMScheduler,
    DPMSolverMultistepInverseScheduler,
    DPMSolverMultistepScheduler,
    DPMSolverSDEScheduler,
    DPMSolverSinglestepScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    HeunDiscreteScheduler,
    KarrasVeScheduler,
    KDPM2AncestralDiscreteScheduler,
    KDPM2DiscreteScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler,
    UniPCMultistepScheduler,
)

from diffusers import DiffusionPipeline, KandinskyPipeline
from compel import Compel
from params import KubinParams
import torch


def use_scheduler(pipeline: KandinskyPipeline, sampler):
    if sampler == "ddim_inverse_sampler":
        pipeline.scheduler = DDIMInverseScheduler.from_config(pipeline.scheduler.config)
    elif sampler == "ddpm_sampler":
        pipeline.scheduler = DDPMScheduler.from_config(pipeline.scheduler.config)
    elif pipeline.scheduler == "dpms_m_sampler":
        pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
            pipeline.scheduler.config
        )
    elif sampler == "ddim_sampler":
        pipeline.scheduler = DDIMScheduler.from_config(pipeline.scheduler.config)


def _encode_and_concat(
    compel: Compel, embeds, negative_embeds, prompt, negative_prompt
):
    embeds = embeds
    negative_embeds = negative_embeds
    compel_embeds = torch.reshape(compel(prompt), embeds.shape)
    compel_negative_embeds = torch.reshape(
        compel(negative_prompt), negative_embeds.shape
    )

    return (compel_embeds, compel_negative_embeds)


def apply_prompt_encoder(k_params: KubinParams, pipeline: DiffusionPipeline):
    if k_params("diffusers", "use_compel_encoder"):
        compel = Compel(
            tokenizer=pipeline.tokenizer, text_encoder=pipeline.text_encoder
        )
        return lambda emb, neg_emb, p, neg_p, compel=compel: _encode_and_concat(
            compel, emb, neg_emb, p, neg_p
        )
    else:
        return lambda embeds, neg_embeds: (embeds, neg_embeds)
