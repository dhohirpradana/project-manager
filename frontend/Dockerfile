# Build stage
FROM node:20-slim as builder

WORKDIR /build

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Runtime stage
FROM node:20-slim

WORKDIR /app

COPY --from=builder /build/package*.json ./
COPY --from=builder /build/.next ./.next
COPY --from=builder /build/public ./public
COPY --from=builder /build/node_modules ./node_modules

USER node

EXPOSE 3000

CMD ["npm", "start"]
