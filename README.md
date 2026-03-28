# Travel Booking Agent2Agent + MCP System

A complete travel booking system with Agent-to-Agent communication using VideoSDK AI agents. The system coordinates between a voice travel agent, flight specialist, hotel specialist, and email automation agent.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

```bash
.venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Environment Variables

Set the following environment variables:

```bash
VIDEOSDK_AUTH_TOKEN="your_videosdk_token"
GOOGLE_API_KEY="your_google_api_key"
ZAPIER_MCP_SERVER="your_mcp_server_url"
```

Get your VideoSDK token at: https://app.videosdk.live

Get your Google AI API key at: https://aistudio.google.com/apikey

### 5. Run the Application

```bash
python main.py
```

## Testing

When you run the application, it will generate a playground URL where you can interact with the AI voice agent. The URL format will be:

```
https://playground.videosdk.live?token=<auto_generated_token>&roomId=<auto_generated_room_id>
```

The system automatically adds the token and roomId that will be used by the client to communicate with the AI voice agent.

## Client Integration

For other client implementations (React, React Native, Android, Flutter, iOS), visit the documentation at:

https://docs.videosdk.live

## Usage

Once connected to the playground, you can:

- Ask about travel destinations
- Request flight bookings
- Request hotel bookings
- Receive email confirmations

Example: "I want to book a trip to Paris for next week"

## VideoSDK Agents

Build and deploy production-ready AI voice & video agents with [VideoSDK](https://videosdk.live). This repo is your central hub for agent templates, feature examples, and everything you need to ship real-world AI-powered applications.

| Resource | Description |
|---|---|
| 🚀 [Use Case Examples](https://github.com/videosdk-live/agents/tree/main/use_case_examples) | Production-ready templates across Customer Support, Healthcare, Tech Support & more |
| ⚡ [Feature Examples](https://github.com/videosdk-live/agents/tree/main/examples) | Always up-to-date examples showcasing the latest VideoSDK Agent features |
| 📖 [AI Agents Docs](https://docs.videosdk.live/ai_agents/introduction) | Full guides, concepts & API references to get you started |

> ⭐ If this helps you, star this repo and [`videosdk-live/agents`](https://github.com/videosdk-live/agents) — it keeps us motivated to ship more!
