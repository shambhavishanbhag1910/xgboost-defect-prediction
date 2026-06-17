# AWS ECS Deployment Steps

Use ECS after EC2 if you want a more professional deployment.

High-level steps:
1. Create ECR repository.
2. Build Docker image.
3. Push image to ECR.
4. Create ECS cluster.
5. Create ECS task definition.
6. Create ECS service.
7. Expose through Application Load Balancer.
8. Test `/health` and `/docs`.

Commands overview:
```bash
aws ecr create-repository --repository-name xgboost-defect-api
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com
docker build -t xgboost-defect-api .
docker tag xgboost-defect-api:latest <account-id>.dkr.ecr.ap-south-1.amazonaws.com/xgboost-defect-api:latest
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/xgboost-defect-api:latest
```
