FROM node:20-alpine

WORKDIR /srv/app
COPY . .
RUN corepack enable && pnpm install --frozen-lockfile && pnpm build

EXPOSE 3000
CMD ["pnpm", "start"]
