from python_a2a import AgentNetwork, A2AClient, AIAgentRouter

# Create an agent network
network = AgentNetwork(name="Travel Assistant Network")

# Add agents to the network
network.add("weather", "http://localhost:5001")
network.add("hotels", "http://localhost:5002")
network.add("attractions", "http://localhost:5003")

# Create a router to intelligently direct queries to the best agent
router = AIAgentRouter(
    llm_client=A2AClient("http://localhost:5000/openai"),  # LLM for making routing decisions
    agent_network=network
)

# Route a query to the appropriate agent
agent_name, confidence = router.route_query("What's the weather like in Paris?")
print(f"Routing to {agent_name} with {confidence:.2f} confidence")

# Get the selected agent and ask the question
agent = network.get_agent(agent_name)
response = agent.ask("What's the weather like in Paris?")
print(f"Response: {response}")

# List all available agents
print("\nAvailable Agents:")
for agent_info in network.list_agents():
    print(f"- {agent_info['name']}: {agent_info['description']}")