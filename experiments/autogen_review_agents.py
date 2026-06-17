from autogen import AssistantAgent

bug_agent = AssistantAgent(
    name="BugReviewer",
    system_message="Review code for bugs."
)

security_agent = AssistantAgent(
    name="SecurityReviewer",
    system_message="Review code for security issues."
)

performance_agent = AssistantAgent(
    name="PerformanceReviewer",
    system_message="Review code for performance issues."
)

print("AutoGen Reviewer Agents Created")
print(bug_agent.name)
print(security_agent.name)
print(performance_agent.name)