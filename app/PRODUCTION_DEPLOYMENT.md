# Production Deployment Guide for vs268.dei.isep.ipp.pt

## Virtual Server Configuration

- **Hostname**: vs268 (vs268.dei.isep.ipp.pt)
- **IPv4**: 10.9.21.12/16 (255.255.0.0)
- **IPv4 Gateway**: 10.9.0.1
- **IPv6**: fd1e:2bae:c6fd:1009::150c/64
- **IPv6 Gateway**: fd1e:2bae:c6fd:1009::1
- **DNS Nameservers**: 192.168.62.32, 192.168.62.8, 192.168.62.4
- **DNS Domain**: dei.isep.ipp.pt

## Public Access Port Mappings

The following ports are mapped from the public gateway to the virtual server:

| Public Port | Gateway | Target Service |
|---|---|---|
| 2222 | vsgate-ssh.dei.isep.ipp.pt:10268 | SSH |
| 2223 | vsgate-s1.dei.isep.ipp.pt:10268 | Service 1 |
| 2224 | vsgate-http.dei.isep.ipp.pt:10268 | **HTTP** (Primary) |
| 2225 | vsgate-s2.dei.isep.ipp.pt:10268 | Service 2 |
| 2226 | vs-gate.dei.isep.ipp.pt:10268 | HTTP/HTTPS |
| 2227 | vsgate-s3.dei.isep.ipp.pt:10268 | Service 3 |
| 2228 | vs-gate.dei.isep.ipp.pt:30268 | HTTP/HTTPS (Alt 1) |
| 2229 | vs-gate.dei.isep.ipp.pt:40268 | HTTP/HTTPS (Alt 2) |

## Deploying the Backend API

### Option 1: Port 8000 (4 workers)

```bash
cd /path/to/app
make serve-prod-8000
```

**Access points**:
- Local: http://10.9.21.12:8000/api/docs
- Public: http://vs268.dei.isep.ipp.pt:8000/api/docs

### Option 2: Port 5000 (4 workers)

```bash
cd /path/to/app
make serve-prod-5000
```

**Access points**:
- Local: http://10.9.21.12:5000/api/docs
- Public: http://vs268.dei.isep.ipp.pt:5000/api/docs

## Frontend Direct Access

If you have an HTTP server running on port 80, it can be accessed through:
- **By IP**: http://10.9.21.12/
- **By hostname**: http://vs268.dei.isep.ipp.pt/

If you have an HTTPS server running on port 443:
- **By IP**: https://10.9.21.12/
- **By hostname**: https://vs268.dei.isep.ipp.pt/

## Environment Configuration

Use the `.env.production` file to configure service settings:

```bash
# Load environment variables
source app/service/.env.production

# Then start the service
make serve-prod-8000
```

### Key Environment Variables

- `SERVICE_PROFILE`: Model profile (leve, regular, pesado)
- `SERVICE_MODEL_VERSION`: Specific model version to load
- `SERVICE_RELOAD_ON_START`: Whether to reload models on startup (false for production)

## CORS Configuration

The backend now supports CORS for the following origins:

- Development: `http://localhost:5173`, `http://localhost:3000`
- Production: `http://10.9.21.12`, `https://10.9.21.12`
- Production: `http://vs268.dei.isep.ipp.pt`, `https://vs268.dei.isep.ipp.pt`

## Recommended Deployment Architecture

For production:

1. **Frontend**: Served on port 80/443 (via nginx, Apache, or similar)
2. **Backend API**: Running on port 8000 (uvicorn with 4 workers)
3. **Reverse Proxy**: nginx or similar to route requests appropriately

Example nginx configuration:
```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name vs268.dei.isep.ipp.pt 10.9.21.12;

    location / {
        root /path/to/frontend/dist;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Health Check

API health endpoint: `/health`

Example:
```bash
curl http://10.9.21.12:8000/health
```

## API Documentation

Once running, access Swagger UI at:
- http://vs268.dei.isep.ipp.pt:8000/api/docs

Or ReDoc at:
- http://vs268.dei.isep.ipp.pt:8000/api/redoc
