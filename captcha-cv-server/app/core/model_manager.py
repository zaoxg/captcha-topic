# -*- coding: utf-8 -*-
# @Time    : 2025/7/10 10:29
# @Author  : zhaoxiangpeng
# @File    : model_manager.py

import torch
from torch.nn import Module

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'


class ModelManager:
    def __init__(self):
        self.models = {}
        self.states = {}

    def load_model(self, name, model_class: Module = None, weights_path=None):
        state = torch.load(weights_path, weights_only=False, map_location=torch.device(DEVICE))
        net = state['net']
        anchors = state['anchors']
        class_types = state['class_types']
        net.eval()
        self.models[name] = state
        return state

    def load_state(self, name, weights_path: str):
        state = torch.load(weights_path, weights_only=False, map_location=torch.device(DEVICE))
        net = state['net']
        anchors = state['anchors']
        class_types = state['class_types']
        net.eval()
        self.states[name] = state
        return state

    def get_model(self, name):
        return self.models.get(name)

    def get_state(self, name):
        return self.states.get(name)


model_manager = ModelManager()
