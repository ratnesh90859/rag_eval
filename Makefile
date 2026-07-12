.PHONY: all ingest backend frontend run clean

all: run

ingest:
	cd backend && python scripts/ingest.py

backend:
	cd backend && uvicorn src.api.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

run:
	docker-compose up --build

trulens:
	cd backend && trulens-eval --port 8501

clean:
	rm -rf backend/chroma_db
	rm -rf frontend/node_modules
	docker-compose down
