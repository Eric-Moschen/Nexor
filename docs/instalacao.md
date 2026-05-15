# Instalacao Local

1. Instale Docker Desktop.
2. Copie `.env.example` para `.env`.
3. Suba os containers:

```powershell
docker compose up --build -d
```

4. Rode migrations e seeds:

```powershell
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_initial_data
```

5. Acesse `http://localhost:5173`.
