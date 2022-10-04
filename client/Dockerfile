FROM node:16-alpine as build-step

WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json

RUN npm install
RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

EXPOSE 3000
CMD ["npm", "start"]
