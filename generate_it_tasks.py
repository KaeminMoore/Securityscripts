import random

# Define base tasks with variations, sub-tasks, and filler tasks
tasks = [
    "Perform system maintenance",
    "Monitor network traffic",
    "Update security patches",
    "Conduct vulnerability assessments",
    "Troubleshoot software issues",
    "Manage cloud resources",
    "Optimize system performance",
    "Backup critical data",
    "Analyze security logs",
    "Assist users with IT issues",
    "Deploy new software updates",
    "Configure firewall rules",
    "Test disaster recovery procedures",
    "Automate repetitive IT tasks",
    "Document system configurations",
    "Audit user permissions",
    "Set up and manage virtual machines",
    "Investigate security alerts",
    "Provide technical support",
    "Research emerging IT threats",
    "Ensure compliance with IT policies",
    "Optimize cloud infrastructure",
    "Respond to security incidents",
    "Evaluate new IT tools",
]

sub_tasks = [
    "Verify system health before starting",
    "Create detailed documentation of the process",
    "Consult IT team for best practices",
    "Perform initial risk assessment",
    "Ensure backup is available before changes",
    "Coordinate with stakeholders before implementation",
    "Test configurations in a sandbox environment",
    "Schedule maintenance during off-peak hours",
    "Review logs after implementation",
    "Provide a report on the findings",
]

filler_tasks = [
    "Attend IT team meeting",
    "Respond to emails from management",
    "Update task tracker with recent activities",
    "Check for pending software license renewals",
    "Assist a colleague with an IT issue",
    "Read industry news for latest trends",
    "Participate in cybersecurity awareness training",
    "Document lessons learned from recent incidents",
    "Test a new IT tool in a lab environment",
    "Evaluate feedback from end-users",
]

# Generate 1,000 tasks with variation
task_list = []
for i in range(1, 1001):
    base_task = random.choice(tasks)
    variation = random.choice(sub_tasks) if random.random() < 0.5 else random.choice(filler_tasks)
    task_list.append(f"{i}. {base_task} - {variation}")

# Write tasks to a text file
output_file = "IT_Specialist_Tasks.txt"
with open(output_file, "w") as file:
    file.write("\n".join(task_list))

print(f"Task list generated and saved as '{output_file}'.")
