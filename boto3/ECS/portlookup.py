import boto3

def get_ecs_task_running_on_port(cluster_name, port,session,region):
    ecs_client = session.client('ecs', region_name=region)

    # Get list of tasks in the cluster
    tasks_response = ecs_client.list_tasks(cluster=cluster_name)
    
    if 'taskArns' not in tasks_response:
        print("No tasks found in the cluster.")
        return
    
    # Describe tasks to get more details
    tasks_details = ecs_client.describe_tasks(
        cluster=cluster_name,
        tasks=tasks_response['taskArns']
    )

    for task in tasks_details['tasks']:
        for container in task['containers']:
            if 'networkBindings' in container:
                for binding in container['networkBindings']:
                    if binding['containerPort'] == port:
                        print(f"ECS Task running on port {port}: {task['taskArn']}")
                        return
    
    print(f"No ECS Task found running on port {port}.")

# Replace 'your_cluster_name' with your actual ECS cluster name
    

cluster_name = '<>'
port = 44334
region = ['eu-west-1', 'us-east-1', 'us-west-2', 'ap-southeast-2' ]

for i in region:
    session = boto3.Session()
    region=i
    get_ecs_task_running_on_port(cluster_name, port,session,region)
