"""
Configuration Package

This package contains configuration and model setup for the voice assistant.
"""

from .models import create_model, create_pipeline, make_context, create_meeting_room

__all__ = ['create_model', 'create_pipeline', 'make_context', 'create_meeting_room'] 