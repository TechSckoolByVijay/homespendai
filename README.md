# Expense Tracking App - Receipt Intelligence

Production-oriented scaffold for a receipt intelligence platform using FastAPI, PostgreSQL, LangGraph, and React + Vite.

## Project Structure

- `backend/` FastAPI service with modular architecture
- `frontend/` React + Vite + Tailwind mobile-first UI
- `docker-compose.yml` local stack with PostgreSQL, pgAdmin, FastAPI, worker

## Backend Highlights

- Routers:
  - `POST /api/receipts/upload`
  - `GET /api/receipts`
  - `GET /api/receipts/{receipt_id}`
  - `DELETE /api/receipts/{receipt_id}`
  - `GET /api/insights/monthly`
  - `GET /api/insights/health`
  - `GET /api/insights/category-breakdown`
  - `GET /api/analytics/spending-trend`
  - `GET /api/analytics/store-frequency`
- Azure integrations:
  - `app/services/storage_service.py` for Azure Blob upload (`user-receipts`)
  - `app/services/ocr_service.py` for Azure Document Intelligence (`prebuilt-receipt`)
- AI pipeline:
  - `app/ai/receipt_graph.py`
  - nodes: extract items, categorize, spending insight, health insight
- Database:
  - SQLAlchemy models for `users`, `receipts`, `receipt_items`, `insights`, `spending_summary`

## Frontend Highlights

- Mobile-first camera-first landing action (`SCAN RECEIPT`)
- Components:
  - `ReceiptScanner.jsx`
  - `ReceiptList.jsx`
  - `InsightsDashboard.jsx`
  - `UploadButton.jsx`
- Vite configured for GitHub Pages base path

## Quick Start (Docker Only)

### 1) Build all services

```powershell
Set-Location "c:\Learning Lab\REPOS\expense-tracking-app"
docker compose build
```

### 2) Run all services

```powershell
Set-Location "c:\Learning Lab\REPOS\expense-tracking-app"
docker compose up -d
```

### 3) Access services

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- pgAdmin: `http://localhost:5050`

### 4) Stop services

```powershell
Set-Location "c:\Learning Lab\REPOS\expense-tracking-app"
docker compose down
```

## Environment Variables

Update `backend/.env.docker` with:

- `DATABASE_URL`
- `AZURE_BLOB_CONNECTION_STRING`
- `AZURE_BLOB_CONTAINER_NAME`
- `AZURE_DOCINTEL_ENDPOINT`
- `AZURE_DOCINTEL_KEY`

`docker-compose.yml` already injects `VITE_API_BASE_URL` at frontend build time.

## Example API Calls

```powershell
$uid = "11111111-1111-1111-1111-111111111111"
Invoke-RestMethod "http://localhost:8000/api/receipts?user_id=$uid" -Method GET
Invoke-RestMethod "http://localhost:8000/api/insights/health?user_id=$uid" -Method GET
Invoke-RestMethod "http://localhost:8000/api/analytics/spending-trend?user_id=$uid" -Method GET
```

Upload example:

```powershell
$uid = "11111111-1111-1111-1111-111111111111"
$form = @{ file = Get-Item "C:\path\to\receipt.jpg" }
Invoke-RestMethod "http://localhost:8000/api/receipts/upload?user_id=$uid" -Method POST -Form $form
```

## Receipt Processing Flow

1. Upload image/PDF
2. Save receipt to Azure Blob Storage
3. Run OCR via Azure Document Intelligence
4. Run LangGraph pipeline (extract -> categorize -> spending insight -> health insight)
5. Persist receipt/items/insights in PostgreSQL
6. Fetch data from receipts/analytics/insights APIs

## Docker Build Targets

Build frontend image only:

```powershell
Set-Location "c:\Learning Lab\REPOS\expense-tracking-app"
docker build -t expense-frontend -f .\frontend\Dockerfile .\frontend
```

Build backend image only:

```powershell
Set-Location "c:\Learning Lab\REPOS\expense-tracking-app"
docker build -t expense-backend -f .\backend\Dockerfile .\backend
```
