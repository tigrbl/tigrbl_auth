FROM node:22-alpine AS build


WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:1.27-alpine

ENV TBA_AUTH_BACKEND_UPSTREAM="http://tba-auth:8000"

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80/tcp
