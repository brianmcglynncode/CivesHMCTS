FROM nginx:alpine

# Copy static assets
COPY webapp /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port and start nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
