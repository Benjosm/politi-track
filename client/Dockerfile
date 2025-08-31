# Use an official Node.js LTS (Long-Term Support) version as a base image
# The 'alpine' variant is lightweight and good for development
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) first
# This leverages Docker's layer caching. The npm install step will only re-run if these files change.
COPY package.json ./
COPY package-lock.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your application's source code into the container
COPY . .

# Vite's default port is 5173. Expose it to the Docker network.
EXPOSE 5173

# The command to run when the container starts.
# We use the "dev" script from package.json which we updated with "--host".
CMD [ "npm", "run", "dev" ]
