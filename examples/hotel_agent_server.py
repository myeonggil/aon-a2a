from python_a2a import A2AServer, skill, agent, run_server, TaskStatus, TaskState

@agent(
    name="Hotel Agent",
    description="Provides hotel information",
    version="1.0.0"
)
class HotelAgent(A2AServer):
    
    @skill(
        name="Get Hotel",
        description="Get hotel for a location",
        tags=["hotel", "location"]
    )
    def get_hotel(self, location):
        """Get hotel for a location."""
        # Mock implementation
        return f"Here is good {location}"
    
    def handle_task(self, task):
        # Extract location from message
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""
        
        if "weather" in text.lower() and "in" in text.lower():
            location = text.split("in", 1)[1].strip().rstrip("?.")
            
            # Get weather and create response
            weather_text = self.get_weather(location)
            task.artifacts = [{
                "parts": [{"type": "text", "text": weather_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={"role": "agent", "content": {"type": "text", 
                         "text": "Please ask about weather in a specific location."}}
            )
        return task

# Run the server
if __name__ == "__main__":
    agent = HotelAgent()
    run_server(agent, port=5002)