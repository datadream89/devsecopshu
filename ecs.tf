provider "aws" {
  region = "us-west-2"
}

resource "aws_ecs_cluster" "webapp-ecs-cluster" {
  name = "ecs-cluster-for-webapp"
}

resource "aws_ecs_service" "webapp-ecs-service" {
  name            = "webapp"
  cluster         = aws_ecs_cluster.webapp-ecs-cluster.id
  task_definition = aws_ecs_task_definition.webapp-ecs-task-definition.arn
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = ["subnet-029982cf20913d8eb"]
    assign_public_ip = true
  }
  desired_count = 1
  load_balancer {
    target_group_arn = "arn:aws:elasticloadbalancing:us-west-2:410529377148:targetgroup/dqwebapp/bb11ccbafaa1932d"
    container_name   = "frontend"
    container_port   = 4200
  }
}

resource "aws_ecs_task_definition" "webapp-ecs-task-definition" {
  family                   = "ecs-task-definition-webapp"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  memory                   = "2048"
  cpu                      = "1024"
  execution_role_arn       = "arn:aws:iam::410529377148:role/ecsTaskExecutionRole"
  container_definitions    = <<EOF
[
  {
    "name": "frontend",
    "image": "410529377148.dkr.ecr.us-west-2.amazonaws.com/dataquality:frontend",
    "memory": 2048,
    "cpu": 1024,
    "essential": true,
    "portMappings": [
      {
        "containerPort": 4200,
        "hostPort": 4200
      }
    ]
  }
]
EOF
}
