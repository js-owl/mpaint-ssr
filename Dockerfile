# Use Node.js 20 Alpine (smaller and more compatible)
FROM node:20-alpine

# Install dependencies for build if needed
RUN apk add --no-cache python3 make g++

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the application
RUN npm run build

# Expose port (adjust if needed)
EXPOSE 3000

# Start preview server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]

