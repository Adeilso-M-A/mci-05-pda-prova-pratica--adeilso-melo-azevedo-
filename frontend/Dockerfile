# Dockerfile do Frontend Angular — Multi-stage Build
# Gerenciador de Chamados — Curso Provisionamento de Aplicações FPFTech

FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --silent
COPY . .
RUN npm run build

FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx-spa.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist/chamados-frontend/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
