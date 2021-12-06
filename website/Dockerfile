FROM node:16.2 as build-stage
WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY ./ /app/

RUN npm run build

FROM nginx:1.15
COPY --from=build-stage /app/build/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf