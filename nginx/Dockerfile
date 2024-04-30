FROM node:21 AS build-stage

WORKDIR /app

COPY ./vue ./
RUN npm install
RUN npm run build

FROM nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html/
COPY ./default.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]