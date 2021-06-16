FROM node

WORKDIR /app/frontend
COPY ./frontend/package.json /app/frontend

RUN npm install

EXPOSE 3000
CMD ["npm", "start"]
