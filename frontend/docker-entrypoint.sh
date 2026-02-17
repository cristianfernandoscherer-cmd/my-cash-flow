#!/bin/sh

# Default value if API_BASE_URL is not set
if [ -z "$API_BASE_URL" ]; then
  API_BASE_URL="http://localhost:8080"
fi

echo "Setting API_BASE_URL to $API_BASE_URL"

# Debug: mostrar o conteúdo antes da substituição
echo "Before replacement:"
grep -n "__API_BASE_URL__" /usr/share/nginx/html/app.js || echo "Placeholder not found!"

# Replace the placeholder in app.js
sed -i "s|__API_BASE_URL__|$API_BASE_URL|g" /usr/share/nginx/html/app.js

# Debug: mostrar depois da substituição
echo "After replacement:"
grep -n "$API_BASE_URL" /usr/share/nginx/html/app.js || echo "Replacement failed!"

# Execute nginx
exec "$@"