#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Text-to-Speech do FHO Bot
Gerencia vozes Azure TTS e Windows SAPI
"""

from .tts_manager import TTSManager
from .azure_tts import AzureTTS
from .windows_sapi_tts import WindowsSAPITTS

__all__ = ['TTSManager', 'AzureTTS', 'WindowsSAPITTS']
