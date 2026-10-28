# Step 1: Use lightweight Node runtime
FROM node:20-alpine

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy package files first
COPY package*.json ./

# Step 4: Install dependencies
RUN npm ci --omit=dev || npm install --omit=dev

# Step 5: Copy application code
COPY . .

# Step 6: Expose port
EXPOSE 5000

# Step 7: Launch the server
CMD ["node", "server.js"]
