#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Tkinter - Interface Visual do FHO Bot
Contém todas as interfaces visuais e aplicações Tkinter do FHO Bot
"""

# Exportar as classes principais para facilitar importação
from .visual_interface import VisualInterface, BotState
from .enhanced_visual import EnhancedVisualInterface

__all__ = [
    'VisualInterface',
    'EnhancedVisualInterface', 
    'BotState'
]

# Informações do módulo
__version__ = "1.0.0"
__author__ = "FHO Bot Team"
__description__ = "Interface visual moderna para o FHO Bot usando Tkinter"
