FROM node:18-alpine as build

WORKDIR /usr/src/app

ADD *.json ./

RUN npm install

ADD ./public ./public
ADD ./src ./src
#COPY . .

RUN npm run build

FROM nginx:stable-alpine
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=build /usr/src/app/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]