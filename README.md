# rabbit

An exploratory API testing exercise. You get information through reference (someone writes authoritatively), inference (you discover patterns), or conference (someone tells you). Here you don't have reference — turn up inference to test this!

## Deployment

Deployed to Railway: two containers, one project

API + UI: https://api-production-d3790.up.railway.app

UI: https://api-production-d3790.up.railway.app/rabbit-ui

Docs: https://api-production-d3790.up.railway.app/docs

The rabbit service runs internally on rabbit.railway.internal:8080 — not exposed to the internet. The api service is the only public endpoint. Cross-service communication goes over Railway's private network.

To redeploy from the current directory (deployment is not linked to GitHub):

```bash
railway up --service rabbit --detach
railway up --service api --detach
```

## Run with Docker (recommended)

Requires Docker with Compose.

```bash
docker compose up --build
```

Two containers start: `rabbit` (compute service, internal) and `api` (API + UI, port 8000).

- API: http://localhost:8000/rabbit/{n} — `n` must be a positive integer ≤ 1473 (larger values overflow)
- UI: http://localhost:8000/rabbit-ui
- Docs: http://localhost:8000/docs

## Run locally

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Start the compute service in one terminal:

```bash
uvicorn rabbit_service:app --port 8080
```

Start the API in another:

```bash
RABBIT_SERVICE_URL=http://localhost:8080 uvicorn main:app --reload
```

## Test

All test tools support running against local or deployed targets.

**pytest**

```bash
# local (auto-starts a server)
pytest tests/

# deployed
BASE_URL=https://api-production-d3790.up.railway.app pytest tests/
```

**Bruno**

Open the `bruno/` folder as a collection in the Bruno app. Select the `local` or `deployed` environment from the environment switcher, then run the requests in the `rabbit/` folder.

**REST Client**

Open `rest-client/read.http` in VS Code with the REST Client extension installed. Uncomment the `@baseUrl` line for your target, then send requests with `Send Request`.

**Schemathesis**

Property-based testing against the OpenAPI spec with Schemathesis:
`uvx schemathesis run http://localhost:8000/openapi.json --header "X-API-Key: aaa"`

If you installed schemathesis
`st run http://localhost:8000/openapi.json --header "X-API-Key: aaa" --report=junit`

## Possible, even recommended tools

Sending requests, looking at responses

- curl
- swagger (the UI for openAPI documentation)
- scalar (the replacement for swagger https://scalar.com/guides/migration/swagger-ui)
- rest client

Sending requests, asserting on responses

- bruno (\*git-first approach)
- postman / insomnia (\*ui first approach)
- soapUI (\*ui first approach)
- programming-language native e.g python - pytest - requests or typescript - playwright (git-only approach)

Default-all asserting for responses

- approvals (library for multiple programming languages)

Generative, with packaged asserts (properties)

- schemathesis
- restler https://github.com/microsoft/restler-fuzzer
- evomaster https://github.com/WebFuzzing/evomaster

Setting up scope of testing by mocking

- wiremock
