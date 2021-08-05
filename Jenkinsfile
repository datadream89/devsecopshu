pipeline {
  agent any
  stages {
    stage('frontend') {
      steps {
         sh script:'''
          #!/bin/bash
          
          echo "This is $(pwd)"
          sudo -n docker system prune --all -f
          aws configure list
          sudo docker login -u AWS -p $(aws ecr get-login-password --region us-west-2) 410529377148.dkr.ecr.us-west-2.amazonaws.com
          sudo -n docker build -t frontend .
          sudo -n docker tag frontend:latest 410529377148.dkr.ecr.us-west-2.amazonaws.com/dataquality:frontend
          sudo -n docker push 410529377148.dkr.ecr.us-west-2.amazonaws.com/dataquality:frontend
        '''
      }
    }
    stage('backend') {
      steps {
         sh script:'''
          #!/bin/bash
          cd ./api
          sudo -n docker system prune --all -f
          sudo -n docker build -t backend .
          sudo -n docker tag backend:latest 410529377148.dkr.ecr.us-west-2.amazonaws.com/dataquality:backend
          sudo -n docker push 410529377148.dkr.ecr.us-west-2.amazonaws.com/dataquality:backend
          aws ecr describe-repositories --output text | awk '{print $6}' | while read line; do  aws ecr list-images --repository-name $line --filter tagStatus=UNTAGGED --query 'imageIds[*]' --output text | while read imageId; do aws ecr batch-delete-image --repository-name $line --image-ids imageDigest=$imageId; done; done
          
        '''
      }
    }
    stage('ecs deploy') {
      steps {
         sh script:'''
          #!/bin/bash
          sudo terraform destroy -auto-approve
          sudo terraform init -input=false
          sudo terraform plan -out=tfplan -input=false
          sudo terraform apply -input=false tfplan
          
        '''
      }
    }
  }
}
