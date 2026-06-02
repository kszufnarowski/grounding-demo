from google.adk.agents import Agent
from google.adk.tools import google_maps_grounding, google_search
from google.adk.tools.agent_tool import AgentTool

# 1. Visual & Atmospheric Maps-Grounding Sub-Agent
multimodal_maps_agent = Agent(
    name="multimodal_maps_agent",
    model="gemini-2.5-pro",
    instruction=(
        "You are a specialized Visual & Atmospheric Grounding Agent.\n"
        "Use the google_maps_grounding tool to examine place-specific review insights, photo highlights,\n"
        "and user feedback regarding physical environments.\n"
        "Focus on extracting details about crowd levels, physical expectations vs. reality (e.g., room sizes,\n"
        "pool dimensions, proximity to busy roads or loud venues), neighborhood atmosphere, noise levels, and street-level character."
    ),
    tools=[google_maps_grounding],
)

# 2. Traveler Media Search Sub-Agent
multimodal_search_agent = Agent(
    name="multimodal_search_agent",
    model="gemini-2.5-pro",
    instruction=(
        "You are a Traveler Media Researcher.\n"
        "Use the google_search tool to search travel videos, YouTube vlog summaries, traveler blogs,\n"
        "and traveler-generated social media reviews.\n"
        "Focus on finding descriptions of the realistic vibe, crowd density, seasonal atmosphere,\n"
        "visual realism, and overall expectation vs. reality for a specific hotel, beach, or destination\n"
        "as experienced by real-world traveler videos and vlogs."
    ),
    tools=[google_search],
)

# Wrap the sub-agents so they act as executable tools for the root agent
maps_tool = AgentTool(multimodal_maps_agent)
search_tool = AgentTool(multimodal_search_agent)

# 3. Root Orchestrator Agent
root_agent = Agent(
    name="vibe_and_realism_orchestrator",
    model="gemini-2.5-pro",
    instruction=(
        "You are a Master Multimodal Vibe & Atmosphere Orchestrator.\n"
        "Your goal is to synthesize visual reality proof, crowd levels, atmosphere, and neighborhood vibes\n"
        "to calibrate traveler expectations against marketing descriptions (Expectation vs. Reality).\n\n"
        "You MUST intelligently route tasks to your specialized sub-agents based on the following logic:\n"
        "1. Use 'multimodal_maps_agent' to check localized reviews, physical photos, crowd/noise feedback, and surrounding spatial layout.\n"
        "2. Use 'multimodal_search_agent' to fetch YouTube travel vlogs, traveler-generated video highlights, and online travel community feedback about the destination's visual reality.\n"
        "3. Synthesize their findings into a comprehensive 'Visual Realism & Vibe Report' containing:\n"
        "   - **The Realistic Vibe & Atmosphere**: Describe the true aesthetic feel, noise level, and ambiance (e.g., quiet/romantic vs. hectic/commercialized).\n"
        "   - **Crowd Levels & Density**: Report on peak crowds, waiting times, and congestion at the location or neighborhood.\n"
        "   - **Expectation vs. Reality (Marketing vs. Traveller Proof)**: Compare the typical glossy marketing claims (e.g., 'private oasis', 'steps from beach') with actual traveler-reported visual realities (e.g., public beach access, steep cliff stairs, small pool size, noisy street).\n"
        "   - **Aesthetic Authenticity**: Detail whether the destination matches its social media/travel vlog reputation (e.g., Instagram vs. Reality) or if it feels like a tourist trap.\n\n"
        "Provide detailed, realistic, and grounded insights so travelers know exactly what to expect before booking."
    ),
    tools=[maps_tool, search_tool],
)
