FROM node:22-alpine

WORKDIR /app

# сначала только package*.json — для кеша npm install
COPY package.json package-lock.json ./

RUN npm install

COPY . .

# прод-сборка
RUN npm run build

# запуск предпросмотра сборки
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]

