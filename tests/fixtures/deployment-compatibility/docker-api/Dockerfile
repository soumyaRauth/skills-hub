FROM node:20-alpine

WORKDIR /srv/app

COPY .env .
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN rm -f .env

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8080/healthz || exit 1

CMD ["npm", "start"]
