# Demo Semantic Bouncer

This is a simple demo of a semantic bouncer using LangChain and Chroma.
The semantic bouncer is a system that uses natural language processing to determine what component of an AI application will handle a request.

## Installation

```sh
uv venv && uv sync
```

## Usage

### Create a collection

First create a JSON file with your texts.

```json
{
    "texts": [
        {
            "content": "Sales report for Q1 2023",
            "route": "sales_report",
            "metadata": {
                "department": "Sales"
            }
        },
        {
            "content": "Get me the latest sales report",
            "route": "sales_report",
            "metadata": {
                "department": "Sales"
            }
        },
        {
            "content": "What is the travel policy?",
            "route": "travel_policy",
            "metadata": {
                "department": "People"
            }
        }
    ]
}
```

Then create the collection

```sh
uv run src/demo_semantic_bouncer/cli.py create \
    --collection abc_co \
    --file examples/abc_co.json
```

### Query a collection

```sh
uv run src/demo_semantic_bouncer/cli.py bouncer \
    --collection abc_co \
    --query 'What is the latest sales report?' \
    --distance 0.2
```

```txt
Best match (0.08220): page_content='Get me the latest sales report' metadata={'department': 'Sales', 'route': 'sales_report'}
Recommended Route: sales_report
```

```sh
uv run src/demo_semantic_bouncer/cli.py bouncer \
    --collection abc_co \
    --query 'What are my employee benefits?' \
    --distance 0.2
```

```txt
Best match (0.47339): page_content='What is the travel policy?' metadata={'route': 'travel_policy', 'department': 'People'}
Recommended Route: agent
```
