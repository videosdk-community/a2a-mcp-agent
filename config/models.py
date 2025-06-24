"""
Model Configuration

This module contains functions for creating and configuring AI models
and pipelines for the voice assistant.
"""

import os
import aiohttp
from videosdk.agents import RealTimePipeline
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from google.genai.types import Modality

def create_model():
    """Create and configure the AI model for the voice agent."""
    
    # Gemini Realtime Configuration
    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        config=GeminiLiveConfig(
            voice="Aoede",  # Valid options: Puck, Charon, Kore, Fenrir, Aoede
            response_modalities=[Modality.AUDIO]
        )
    )
    
    # Alternative OpenAI Configuration (commented out)
    # from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig, TurnDetection
    # model = OpenAIRealtime(
    #     model="gpt-4o-realtime-preview",
    #     config=OpenAIRealtimeConfig(
    #         voice="alloy", # alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, and verse
    #         modalities=["text", "audio"],
    #         turn_detection=TurnDetection(
    #             type="server_vad",
    #             threshold=0.5,
    #             prefix_padding_ms=300,
    #             silence_duration_ms=200,
    #         ),
    #         tool_choice="auto"
    #     )
    # )
    
    # Alternative Nova Sonic Configuration (commented out)
    # from videosdk.plugins.amazon import NovaSonicRealtime, NovaSonicConfig
    # model = NovaSonicRealtime(
    #     model="amazon.nova-sonic-v1:0",
    #     config=NovaSonicConfig(
    #         voice="tiffany",
    #         temperature=0.7,
    #         top_p=0.9,
    #         max_tokens=1024
    #     )
    # )
    
    return model


def create_pipeline(model):
    """Create a RealTimePipeline with the given model."""
    return RealTimePipeline(model=model)


async def create_meeting_room():
    """Create a new meeting room using VideoSDK API."""
    auth_token = os.getenv('VIDEOSDK_AUTH_TOKEN')
    if not auth_token:
        raise ValueError("VIDEOSDK_AUTH_TOKEN environment variable is required")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://api.videosdk.live/v2/rooms',
            headers={'Authorization': auth_token}
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data['roomId']
            else:
                raise Exception(f"Failed to create room: {response.status}")


async def make_context():
    """Create the context for the agent session with dynamic meetingId."""
    meeting_id = await create_meeting_room()
    return {
        "meetingId": meeting_id,
        "name": "Sandbox Agent", 
        "playground": True
    } 