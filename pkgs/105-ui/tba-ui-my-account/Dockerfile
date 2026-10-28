FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
COPY pkgs/105-ui/tba-ui-my-account/package.json pkgs/105-ui/tba-ui-my-account/package.json
RUN npm install
COPY pkgs/105-ui/tba-ui-my-account pkgs/105-ui/tba-ui-my-account
RUN npm run build -w @tba/ui-my-account

FROM nginx:1.27-alpine
COPY --from=build /app/pkgs/105-ui/tba-ui-my-account/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 80
