FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
COPY pkgs/100-uix-core/uix-core/package.json pkgs/100-uix-core/uix-core/package.json
COPY pkgs/105-ui/demo-hub-uix/package.json pkgs/105-ui/demo-hub-uix/package.json
RUN npm install
COPY pkgs/100-uix-core/uix-core pkgs/100-uix-core/uix-core
COPY pkgs/105-ui/demo-hub-uix pkgs/105-ui/demo-hub-uix
RUN npm run build -w @tigrbl-auth/demo-hub-uix

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/pkgs/105-ui/demo-hub-uix/dist /usr/share/demo-hub
COPY pkgs/105-ui/demo-hub-uix/server.mjs /app/server.mjs
EXPOSE 80
CMD ["node", "/app/server.mjs"]
