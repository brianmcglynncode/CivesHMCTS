FROM nginx:alpine

# Copy static assets
COPY webapp /usr/share/nginx/html

# Copy custom nginx config to templates dir for env var substitution
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Default PORT to 80 if not set
ENV PORT=80

# Expose port (metadata)
EXPOSE 80

# Use default entrypoint which runs envsubst
CMD ["nginx", "-g", "daemon off;"]
