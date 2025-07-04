FROM node:latest
LABEL authors="max"

COPY frontend/package.json .
RUN npm install

COPY frontend .
RUN npm run build