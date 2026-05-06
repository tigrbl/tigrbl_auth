FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
ENV VITE_PLATFORM_ENABLE_BRANDING_SETTINGS="true"
ENV VITE_PLATFORM_ENABLE_ADAPTER_SETTINGS="true"
RUN npm run build

FROM nginx:1.27-alpine

ENV TIGRBL_AUTH_BACKEND_UPSTREAM="http://tigrbl-auth:8000"

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80
