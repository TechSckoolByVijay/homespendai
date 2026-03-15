You are a senior software architect helping build a production-ready AI-powered receipt intelligence system.

The goal is to build a mobile-first web application that allows users to scan or upload receipts. The backend processes receipts using OCR and AI to extract spending data and generate insights.

The system should be designed as a scalable microservice-friendly architecture using FastAPI and PostgreSQL, with React + Vite frontend hosted on GitHub Pages.

The system must be modular, cleanly structured, and follow modern backend architecture patterns.

----------------------------------------------------
HIGH LEVEL PRODUCT DESCRIPTION
----------------------------------------------------

Users upload receipts (images or PDFs).

The system will:

1. Store the uploaded file in Azure Blob Storage
2. Extract text using Azure Document Intelligence (OCR)
3. Process extracted text using a LangGraph or langraph pipeline whichever suitable
4. Extract items, prices, store information
5. Categorize purchases
6. Generate insights about spending, habits, and health
7. Store structured data in PostgreSQL
8. Provide APIs to fetch receipts, analytics, and insights

The frontend will be mobile-first with a camera-first interface.

----------------------------------------------------
TECH STACK
----------------------------------------------------

Backend:
- Python
- FastAPI
- Pydantic models
- PostgreSQL
- SQLAlchemy
- LangGraph
- Azure Document Intelligence for OCR
- Azure Blob Storage for file storage

Frontend:
- React
- Vite
- TailwindCSS
- Hosted on GitHub Pages

Infrastructure:
- Docker Compose for local development
- pgAdmin for database management

----------------------------------------------------
BACKEND PROJECT STRUCTURE
----------------------------------------------------

Create a clean modular FastAPI structure.

backend/
    app/
        main.py
        config.py

        routers/
            auth_router.py
            receipt_router.py
            insights_router.py
            analytics_router.py
            health_router.py

        services/
            receipt_service.py
            ocr_service.py
            insight_service.py
            analytics_service.py
            storage_service.py

        ai/
            receipt_graph.py
            nodes/
                extract_items_node.py
                categorize_items_node.py
                spending_insight_node.py
                health_insight_node.py

        models/
            user_model.py
            receipt_model.py
            item_model.py
            insight_model.py

        schemas/
            receipt_schema.py
            insight_schema.py
            analytics_schema.py

        database/
            db.py
            base.py
            session.py

        repositories/
            receipt_repository.py
            insight_repository.py
            user_repository.py

        utils/
            image_utils.py
            parsing_utils.py

----------------------------------------------------
API ROUTER DESIGN
----------------------------------------------------

Use FastAPI routers to bundle APIs by domain.

Example router structure:

auth_router
receipt_router
insight_router
analytics_router

Each router should be registered in main.py.

Example:

/api/auth
/api/receipts
/api/insights
/api/analytics

Example receipt endpoints:

POST /api/receipts/upload
GET /api/receipts
GET /api/receipts/{receipt_id}
DELETE /api/receipts/{receipt_id}

Insights endpoints:

GET /api/insights/monthly
GET /api/insights/health
GET /api/insights/category-breakdown

Analytics endpoints:

GET /api/analytics/spending-trend
GET /api/analytics/store-frequency

All request and response models must use Pydantic.

----------------------------------------------------
PYDANTIC MODELS
----------------------------------------------------

Define clean Pydantic schemas for API validation.

Example ReceiptCreate:

class ReceiptUpload(BaseModel):
    user_id: UUID
    image_url: str

Example ReceiptResponse:

class ReceiptResponse(BaseModel):
    id: UUID
    store_name: str
    purchase_date: datetime
    total_amount: float
    items: List[ReceiptItem]

Example ReceiptItem:

class ReceiptItem(BaseModel):
    item_name: str
    category: Optional[str]
    price: float
    quantity: Optional[int]

----------------------------------------------------
DATABASE DESIGN
----------------------------------------------------

Use PostgreSQL.

Support semi-structured receipt data using JSONB.

Tables:

users
receipts
receipt_items
insights
spending_summary

Receipts table:

id
user_id
store_name
purchase_date
total_amount
raw_ocr_json (JSONB)
image_url
created_at

Items table:

id
receipt_id
item_name
category
price
quantity
metadata JSONB

Insights table:

id
user_id
insight_type
insight_data JSONB
created_at

----------------------------------------------------
AZURE DOCUMENT INTELLIGENCE (OCR)
----------------------------------------------------

Use Azure Document Intelligence for OCR extraction.

Create a service module:

ocr_service.py

Responsibilities:

- Send receipt image to Azure Document Intelligence
- Extract structured receipt data
- Return parsed JSON

Use the prebuilt receipt model if available.

Handle:

store name
date
items
prices
total

----------------------------------------------------
AZURE BLOB STORAGE
----------------------------------------------------

User uploaded receipts should be stored in Azure Blob Storage.

Create storage_service.py.

Responsibilities:

- Upload receipt image
- Generate blob URL
- Store URL in database
- Retrieve receipt file

Use container:

user-receipts

Binary files stored:

images
PDF receipts

----------------------------------------------------
LANGGRAPH RECEIPT PROCESSING PIPELINE
----------------------------------------------------

Implement a LangGraph workflow for processing receipts.

Graph nodes:

1 OCR Node
2 Item Extraction Node
3 Category Mapping Node
4 Spending Insight Node
5 Health Insight Node
6 Persist Data Node

Pipeline flow:

receipt uploaded
→ OCR extraction
→ item parsing
→ category classification
→ insight generation
→ save to database

Graph definition should exist in:

ai/receipt_graph.py

Each node should exist in:

ai/nodes/

----------------------------------------------------
DOCKER COMPOSE (LOCAL DEVELOPMENT)
----------------------------------------------------

docker-compose services:

fastapi
postgres
pgadmin
worker

Postgres:
port 5432

pgadmin:
port 5050

Mount volumes for persistence.

----------------------------------------------------
FRONTEND (REACT + VITE)
----------------------------------------------------

Frontend should be optimized for mobile first UI.

Framework:
React

Build tool:
Vite

Styling:
TailwindCSS

Structure:

frontend/

src/
    components/
        ReceiptScanner.jsx
        ReceiptList.jsx
        InsightsDashboard.jsx
        UploadButton.jsx

    pages/
        Home.jsx
        Receipts.jsx
        Insights.jsx

    services/
        api.js

    hooks/
        useReceipts.js
        useInsights.js

----------------------------------------------------
MOBILE-FIRST UX
----------------------------------------------------

When user opens the application:

Primary action must be:

SCAN RECEIPT

Large camera button.

Flow:

open app
→ open camera
→ capture receipt
→ upload
→ processing
→ show insights

Support:

camera upload
file upload
pdf upload

----------------------------------------------------
FRONTEND HOSTING
----------------------------------------------------

The frontend will be deployed to GitHub Pages.

Use:

vite build

Then deploy /dist folder to GitHub Pages.

API backend will run separately on cloud infrastructure.

Configure API base URL via environment variables.

----------------------------------------------------
FUTURE EXTENSIBILITY
----------------------------------------------------

Design APIs to support:

mobile app (WebView)
real-time insights
coupon recommendations
shopping optimization
budget forecasting

----------------------------------------------------
OUTPUT REQUIREMENTS
----------------------------------------------------

Generate:

1 Complete FastAPI project structure
2 Router implementations
3 Pydantic models
4 Azure Blob storage integration
5 Azure Document Intelligence integration
6 LangGraph receipt processing pipeline
7 PostgreSQL models
8 Docker Compose setup
9 React + Vite frontend scaffold
10 Example API calls
11 Example receipt processing flow

Code must follow production-grade architecture, modular design, and scalability best practices.