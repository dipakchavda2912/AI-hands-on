# Production Deployment Guide

Complete guide to deploying CodeBaseOpsAI as a production service.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Monitoring & Observability](#monitoring--observability)
6. [Scaling](#scaling)
7. [Security](#security)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Google AI API key
- (Optional) GitHub API token
- (Optional) LangSmith API key for observability

### Installation

```bash
# Clone repository
cd CodeBaseOpsAI-v2

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-production.txt

# Configure environment
cp .env.production .env
# Edit .env with your API keys
```

### Run Examples

```bash
# Run the example application
python main.py
```

---

## 💻 Local Development

### Running the API Server

```bash
# Install API dependencies
pip install -r requirements-api.txt

# Run the server
uvicorn api_server:app --reload --port 8000
```

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Execute agent
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Clone repository dipakchavda2912/base-serverless",
    "thread_id": "test_session"
  }'

# Stream responses
curl -X POST http://localhost:8000/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"request": "Read repository files"}'
```

### Using the Python Client

```bash
# Run example client
python api_client_example.py
```

---

## 🐳 Docker Deployment

### Build Image

```bash
# Build the Docker image
docker build -t codebaseopsai:latest .

# Run the container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -e MODEL_NAME=gemini-2.0-flash-exp \
  codebaseopsai:latest
```

### Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

**Services included:**
- **API Server** (port 8000)
- **Redis** for caching (port 6379)
- **Prometheus** for metrics (port 9090)
- **Grafana** for dashboards (port 3000)

### Access Services

- API: http://localhost:8000/docs (Swagger UI)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

## ☁️ Cloud Deployment

### AWS Deployment (ECS/Fargate)

```bash
# 1. Push image to ECR
aws ecr create-repository --repository-name codebaseopsai
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account}.dkr.ecr.us-east-1.amazonaws.com
docker tag codebaseopsai:latest {account}.dkr.ecr.us-east-1.amazonaws.com/codebaseopsai:latest
docker push {account}.dkr.ecr.us-east-1.amazonaws.com/codebaseopsai:latest

# 2. Create ECS task definition (see aws-task-definition.json)

# 3. Create ECS service
aws ecs create-service \
  --cluster production \
  --service-name codebaseopsai \
  --task-definition codebaseopsai:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

### Google Cloud Run

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/{project-id}/codebaseopsai

# 2. Deploy to Cloud Run
gcloud run deploy codebaseopsai \
  --image gcr.io/{project-id}/codebaseopsai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MODEL_NAME=gemini-2.0-flash-exp \
  --set-secrets GOOGLE_API_KEY=google-api-key:latest
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codebaseopsai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: codebaseopsai
  template:
    metadata:
      labels:
        app: codebaseopsai
    spec:
      containers:
      - name: api
        image: codebaseopsai:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_NAME
          value: "gemini-2.0-flash-exp"
        envFrom:
        - secretRef:
            name: api-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: codebaseopsai
spec:
  selector:
    app: codebaseopsai
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

```bash
# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml
```

---

## 📊 Monitoring & Observability

### LangSmith Integration

```bash
# Enable in .env
ENABLE_TRACING=true
LANGSMITH_API_KEY=your_key
LANGSMITH_PROJECT=production

# View traces at: https://smith.langchain.com
```

### Prometheus Metrics

```python
# Add to api_server.py
from prometheus_client import Counter, Histogram, make_asgi_app

REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

### Sentry Error Tracking

```python
# Add to api_server.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production",
    traces_sample_rate=1.0,
)
```

### Grafana Dashboard

Import `grafana-dashboard.json` for pre-configured monitoring:
- Request rate
- Response time (p50, p95, p99)
- Error rate
- Token usage
- Cache hit rate

---

## 📈 Scaling

### Horizontal Scaling

```bash
# Docker Compose
docker-compose up -d --scale api=5

# Kubernetes
kubectl scale deployment codebaseopsai --replicas=10

# AWS ECS
aws ecs update-service \
  --cluster production \
  --service codebaseopsai \
  --desired-count 10
```

### Auto-scaling

**Kubernetes HPA:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: codebaseopsai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: codebaseopsai
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Balancing

**Nginx Configuration:**
```nginx
upstream codebaseopsai {
    least_conn;
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://codebaseopsai;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Caching Strategy

```python
# Add Redis caching
import redis
from functools import lru_cache

redis_client = redis.Redis(host='redis', port=6379)

@lru_cache(maxsize=1000)
def cached_agent_run(request: str, thread_id: str):
    cache_key = f"agent:{thread_id}:{hash(request)}"
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Execute
    result = agent.run(request, thread_id)
    
    # Cache result (5 min TTL)
    redis_client.setex(cache_key, 300, json.dumps(result))
    
    return result
```

---

## 🔐 Security

### Environment Variables

```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use secrets management
# AWS: AWS Secrets Manager
# GCP: Google Secret Manager
# K8s: Kubernetes Secrets
```

### API Authentication

```python
# Add JWT authentication
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/agent/run")
async def run_agent(
    request: AgentRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify JWT token
    verify_token(credentials.credentials)
    
    # Execute agent
    result = await agent.run_async(request.request)
    return result
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/agent/run")
@limiter.limit("10/minute")
async def run_agent(request: Request, agent_request: AgentRequest):
    # Rate limited to 10 requests per minute per IP
    pass
```

### Input Validation

```python
from pydantic import validator

class AgentRequest(BaseModel):
    request: str
    
    @validator('request')
    def validate_request(cls, v):
        # Sanitize input
        if len(v) > 2000:
            raise ValueError("Request too long")
        
        # Block malicious patterns
        forbidden = ['rm -rf', 'DROP TABLE']
        if any(pattern in v for pattern in forbidden):
            raise ValueError("Invalid request")
        
        return v
```

---

## 🧪 Testing in Production

### Load Testing

```bash
# Install Locust
pip install locust

# Run load test
locust -f tests/load_test.py --host=http://localhost:8000
```

### Integration Tests

```bash
# Run integration tests
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Smoke Tests

```bash
# Quick production health check
./scripts/smoke_test.sh production_url
```

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue: High latency**
- Enable caching
- Increase worker count
- Use async endpoints
- Check network latency to LLM API

**Issue: Memory leaks**
- Monitor with Prometheus
- Check checkpointer cleanup
- Review conversation thread management

**Issue: Rate limiting from LLM**
- Implement exponential backoff
- Use multiple API keys
- Add request queue

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Detailed metrics
curl http://localhost:8000/metrics

# Container health
docker ps
docker logs api
```

---

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] Secrets in secure storage
- [ ] Logging configured
- [ ] Monitoring enabled (LangSmith/Prometheus)
- [ ] Error tracking enabled (Sentry)
- [ ] Rate limiting configured
- [ ] Authentication enabled
- [ ] HTTPS/TLS configured
- [ ] Auto-scaling configured
- [ ] Backups configured (Redis/Database)
- [ ] CI/CD pipeline set up
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] On-call rotation defined

---

**Your production-grade agent is ready to deploy!** 🚀
