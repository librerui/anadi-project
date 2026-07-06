cd service

# Run the API in production mode in the background
mkdir -p /deploy/logs
nohup make serve-prod > /deploy/logs/serve-prod.log 2>&1 &