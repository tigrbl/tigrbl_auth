FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
COPY pkgs/105-ui/tba-ui-my-account/package.json pkgs/105-ui/tba-ui-my-account/package.json
COPY pkgs/100-uix-core/tba-ui-primitives pkgs/100-uix-core/tba-ui-primitives
RUN npm install
COPY pkgs/105-ui/tba-ui-my-account pkgs/105-ui/tba-ui-my-account
RUN npm run build -w @tba/ui-my-account

FROM nginx:1.30.7-alpine@sha256:caf4e1e032a20f9c3c5e28fc7f25ffd768ad8677b4975c54193075997b3a97e3
COPY --from=build /app/pkgs/105-ui/tba-ui-my-account/dist /usr/share/nginx/html
COPY pkgs/105-ui/tba-ui-my-account/nginx.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 80
