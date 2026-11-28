FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
COPY pkgs/100-uix-core/tba-ui-primitives/package.json pkgs/100-uix-core/tba-ui-primitives/package.json
COPY pkgs/105-ui/tba-ui-demo-hub/package.json pkgs/105-ui/tba-ui-demo-hub/package.json
RUN npm install
COPY pkgs/100-uix-core/tba-ui-primitives pkgs/100-uix-core/tba-ui-primitives
COPY pkgs/105-ui/tba-ui-demo-hub pkgs/105-ui/tba-ui-demo-hub
RUN npm run build -w @tba/ui-demo-hub

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/pkgs/105-ui/tba-ui-demo-hub/dist /usr/share/demo-hub
COPY pkgs/105-ui/tba-ui-demo-hub/server.mjs /app/server.mjs
EXPOSE 80
CMD ["node", "/app/server.mjs"]
