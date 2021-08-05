FROM node

# set up angular cli
RUN npm install -g @angular/cli

WORKDIR /app
COPY package.json /app
COPY . /app

# create dist
RUN npm install --save-dev @angular-devkit/build-angular --force
RUN npm install firebase @angular/fire
RUN npm install ng-http-loader@8 --save
CMD ["ng","serve","--host", "0.0.0.0","--disable-host-check"]

