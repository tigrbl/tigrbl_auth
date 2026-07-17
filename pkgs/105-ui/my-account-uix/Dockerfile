FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
COPY pkgs/105-ui/my-account-uix/package.json pkgs/105-ui/my-account-uix/package.json
RUN npm install
COPY pkgs/105-ui/my-account-uix pkgs/105-ui/my-account-uix
RUN npm run build -w @tigrbl-auth/my-account-uix

FROM nginx:1.27-alpine
COPY --from=build /app/pkgs/105-ui/my-account-uix/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 80
