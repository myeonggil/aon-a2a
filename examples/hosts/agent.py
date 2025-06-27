from aon_a2a.hosts.host_agent import HostAgent


root_agent = HostAgent(
    [
        "http://localhost:10001",
        "http://localhost:10001"
    ]
).create_agent()
