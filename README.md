# Receipt Processor API

## Setup (Docker)

```bash
docker build -t receipt-processor .
docker run -p 5000:5000 receipt-processor
```

## Endpoints

### POST /receipts/process

Request:
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [{"shortDescription": "Item", "price": "5.00"}],
  "total": "5.00"
}
```

Response:
```json
{ "id": "your-generated-id" }
```

### GET /receipts/{id}/points

Response:
```json
{ "points": 28 }
```