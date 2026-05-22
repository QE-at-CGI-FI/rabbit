# rabbit

An exploratory API testing exercise. You get information through reference (someone writes authoritatively), inference (you discover patterns), or conference (someone tells you). Here you don't have reference — turn up inference to test this!

## Install

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

- API: http://localhost:8000/rabbit/{n}  — `n` must be a positive integer ≤ 1473 (larger values overflow)
- UI: http://localhost:8000/rabbit-ui
- Docs: http://localhost:8000/docs

## Test

**pytest**

```bash
pytest tests/
```

**Bruno**

Open the `bruno/` folder as a collection in the Bruno app and run the requests in the `rabbit/` folder.

**REST Client**

Open `rest-client/read.http` in VS Code with the REST Client extension installed and send requests with `Send Request`.

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

Setting up scope of testing by mocking

- wiremock
