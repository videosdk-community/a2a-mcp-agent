from videosdk.agents import AgentSession, Pipeline
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from google.genai.types import Modality
from typing import Dict, Any, Optional
import os
import asyncio

# Import agents
from agents.travel_agent import TravelAgent
from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent
from agents.email_agent import EmailAgent


def create_main_pipeline() -> Pipeline:
    """Create pipeline for main voice agent (audio-enabled)"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini integration")
    
    model = GeminiRealtime(
        model=""gemini-3.1-flash-live-preview"-flash-exp",
        api_key=google_api_key,
        config=GeminiLiveConfig(
            voice="Aoede",
            response_modalities=[Modality.AUDIO]
        )
    )
    return Pipeline(llm=model)

def create_specialist_pipeline() -> Pipeline:
    """Create pipeline for specialist agents (text-only)"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini integration")
    
    model = GeminiRealtime(
        model=""gemini-3.1-flash-live-preview"-flash-exp",
        api_key=google_api_key,
        config=GeminiLiveConfig(
            response_modalities=[Modality.TEXT]
        )
    )
    return Pipeline(llm=model)


def create_session(agent: Any, pipeline: Pipeline, context: Dict[str, Any]) -> AgentSession:
    """Create agent session with pipeline and context."""
    return AgentSession(agent=agent, pipeline=pipeline, context=context)


async def create_videosdk_meeting() -> str:
    """Create a VideoSDK meeting room dynamically."""
    import aiohttp
    
    auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
    if not auth_token:
        raise ValueError("VIDEOSDK_AUTH_TOKEN environment variable is required")
    
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": f"{auth_token}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("roomId")
            else:
                raise Exception(f"Failed to create meeting room: {response.status}")


async def start_travel_agents_for_room(meeting_id: str):
    """Start all travel agents for a specific room"""
    print(f"[{meeting_id}] Initializing Travel Booking A2A agent operations...")

    # Validate environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print(f"[{meeting_id}] ERROR: GOOGLE_API_KEY not set in environment variables.")
        return

    try:
        # --- Travel Agent Setup ---
        travel_agent = TravelAgent()
        travel_pipeline = create_main_pipeline()
        travel_session = create_session(travel_agent, travel_pipeline, {
            "roomId": meeting_id,
            "name": "Travel Agent",
            "join_meeting": True,
            "playground": True
        })

        # --- Flight Agent Setup ---
        flight_agent = FlightAgent()
        flight_pipeline = create_specialist_pipeline()
        flight_session = create_session(flight_agent, flight_pipeline, {
            "join_meeting": False,
        })

        # --- Hotel Agent Setup ---
        hotel_agent = HotelAgent()
        hotel_pipeline = create_specialist_pipeline()
        hotel_session = create_session(hotel_agent, hotel_pipeline, {
            "join_meeting": False,
        })

        # --- Email Agent Setup ---
        email_agent = EmailAgent()
        email_pipeline = create_specialist_pipeline()
        email_session = create_session(email_agent, email_pipeline, {
            "join_meeting": False,
        })

        print(f"[{meeting_id}] Starting specialist agents first...")
        # Start specialist agents as background tasks
        flight_task = asyncio.create_task(flight_session.start())
        hotel_task = asyncio.create_task(hotel_session.start())
        email_task = asyncio.create_task(email_session.start())
        
        # Give specialist agents time to initialize and register with A2A
        await asyncio.sleep(3)
        print(f"[{meeting_id}] ✅ All specialist agents should be registered now")
        
        print(f"[{meeting_id}] Starting main travel agent...")
        travel_task = asyncio.create_task(travel_session.start())
        
        print(f"[{meeting_id}] All Travel Booking A2A agents started and running...")
        print(f"[{meeting_id}] System is ready for user interaction. Keeping agents alive...")
        
        # Keep the system running indefinitely until interrupted
        try:
            await asyncio.Event().wait()  # Wait forever
        except asyncio.CancelledError:
            pass
        
        # Cancel all tasks when shutting down
        for task in [travel_task, flight_task, hotel_task, email_task]:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        print(f"[{meeting_id}] Travel Booking A2A agent sessions completed their lifecycle.")

        # Cleanup A2A registrations
        try:
            await travel_agent.unregister_a2a()
            await flight_agent.unregister_a2a()
            await hotel_agent.unregister_a2a()
            await email_agent.unregister_a2a()
        except Exception as e:
            print(f"[{meeting_id}] Error during A2A cleanup: {e}")

    except Exception as ex:
        print(f"[{meeting_id}] [ERROR] during Travel Booking A2A agent setup or runtime: {ex}")
        import traceback
        traceback.print_exc()


async def cleanup_session(meeting_id: str) -> bool:
    """Cleanup session for a meeting room"""
    print(f"[{meeting_id}] Cleanup completed.")
    return True 