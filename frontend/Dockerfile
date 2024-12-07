# Use Node.js as the base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json .

RUN npm install

# Install dependencies

# Copy the rest of the app's files
COPY . .

# Expose port 3000 inside the container
EXPOSE 3000

CMD ["npm", "start"]