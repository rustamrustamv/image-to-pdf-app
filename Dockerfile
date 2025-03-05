# Build React Frontend
FROM node:16 AS client-build
WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client/ .
RUN npm run build

# Build Flask Backend
FROM python:3.9-slim
WORKDIR /app
COPY server/requirements.txt .
RUN pip install -r requirements.txt
COPY server/ .
COPY --from=client-build /app/client/build /app/client/build

EXPOSE 3000
CMD ["python", "app.py"]