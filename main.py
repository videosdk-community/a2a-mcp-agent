#!/usr/bin/env python3
"""
Meeting Scheduler with A2A Communication

This application provides a complete meeting scheduling system with:
- Voice-enabled personal assistant
- Meeting scheduling coordination
- Google Calendar integration via MCP
- Email notifications via MCP

Following the VideoSDK travel example pattern for A2A implementation.
"""

import asyncio
import os
from session_manager import start_travel_agents_for_room, create_videosdk_meeting, cleanup_session

def validate_environment():
    """Validate required environment variables"""
    required_vars = ["VIDEOSDK_AUTH_TOKEN", "GOOGLE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease set these environment variables and try again.")
        return False
    
    return True

async def main():
    """Main entry point for the travel booking system"""
    print("🚀 Starting Travel Booking with A2A Communication")
    print("=" * 60)
    
    # Validate environment
    if not validate_environment():
        return
    
    print("✅ Environment validation passed")
    
    meeting_id = None
    
    try:
        # Create meeting room
        print("🏗️  Creating VideoSDK meeting room...")
        meeting_id = await create_videosdk_meeting()
        print(f"📅 Meeting room created: {meeting_id}")
        
        print("\n🤖 Starting travel booking agents...")
        print("📋 System will coordinate:")
        print("   • Voice interaction with customers")
        print("   • Flight booking coordination")
        print("   • Hotel booking coordination")
        print("   • Email confirmations")
        print("\n⏹️  Press Ctrl+C to shutdown...\n")
        
        # Start all agents (this runs until interrupted)
        await start_travel_agents_for_room(meeting_id)
        
    except KeyboardInterrupt:
        print("\n⚠️  Received interrupt signal, shutting down...")
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if meeting_id:
            print("🧹 Cleaning up resources...")
            success = await cleanup_session(meeting_id)
            if success:
                print(f"✅ Successfully cleaned up meeting {meeting_id}")
            else:
                print(f"⚠️  Meeting {meeting_id} was already cleaned up")
        
        print("👋 Travel booking system shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
