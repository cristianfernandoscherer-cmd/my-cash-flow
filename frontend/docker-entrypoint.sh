#!/bin/sh

# Default value if API_BASE_URL is not set
if [ -z "$API_BASE_URL" ]; then
  API_BASE_URL="http://localhost:8080"
fi

echo "Setting API_BASE_URL to $API_BASE_URL"

# Replace the placeholder in app.js
# We use | as delimiter because URL contains /
sed -i "s|__API_BASE_URL__|$API_BASE_URL|g" /usr/share/nginx/html/app.js

# Execute nginx
exec "$@"
