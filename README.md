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
https://playground.videosdk.live?token=<auto_generated_token>&meetingId=<auto_generated_meeting_id>
```

The system automatically adds the token and meetingId that will be used by the client to communicate with the AI voice agent.

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
