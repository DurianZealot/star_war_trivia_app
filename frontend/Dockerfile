FROM node:18
WORKDIR /frontend
COPY package.json package-lock.json /frontend/
RUN npm cache clean --force
RUN npm install
COPY . /frontend
CMD ["npm", "start"]
