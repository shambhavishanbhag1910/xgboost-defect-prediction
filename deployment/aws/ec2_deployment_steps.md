# AWS EC2 Deployment Steps

## 1. Create EC2 instance
Use Ubuntu 22.04. For testing, use t2.micro/t3.micro. Open inbound ports 22 and 8000.

## 2. SSH into EC2
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

## 3. Install Docker and Git
```bash
sudo apt update
sudo apt install -y docker.io git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```
Logout and login again.

## 4. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/aws-xgboost-defect-prediction.git
cd aws-xgboost-defect-prediction
```

## 5. Build and run
```bash
docker build -t xgboost-defect-api .
docker run -d -p 8000:8000 --name defect-api xgboost-defect-api
```

## 6. Test
```bash
curl http://YOUR_EC2_PUBLIC_IP:8000/health
```
Open:
```text
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

## 7. Proof screenshots
Capture EC2 running, Docker running, `/health`, `/docs`, and `/predict` output.
