cd frontend

npx vite build

cd dist

# Run the frontend in production mode in the background
mkdir -p /deploy/logs
nohup python3 -m http.server 2226 > /deploy/logs/frontend.log 2>&1 &