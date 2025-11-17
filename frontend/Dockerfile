FROM node:22-alpine

WORKDIR /app
COPY package.json vite.config.mts ./
COPY src ./src

RUN npm install
RUN npm run build

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
