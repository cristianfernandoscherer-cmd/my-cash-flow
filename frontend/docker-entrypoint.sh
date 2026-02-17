#!/bin/sh

# Default value if API_BASE_URL is not set
if [ -z "$API_BASE_URL" ]; then
  API_BASE_URL="http://localhost:8080"
fi

echo "Setting API_BASE_URL to $API_BASE_URL"

# Debug: listar arquivos
echo "Listing files in /usr/share/nginx/html:"
ls -la /usr/share/nginx/html/

# Debug: mostrar conteúdo do index.html (primeiras linhas)
echo "Content of index.html (first 10 lines):"
head -10 /usr/share/nginx/html/index.html || echo "index.html not found!"

# Replace the placeholder in app.js
sed -i "s|__API_BASE_URL__|$API_BASE_URL|g" /usr/share/nginx/html/app.js

# Execute nginx
exec "$@"