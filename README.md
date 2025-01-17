# pydantic-demo
Demo of some pydantic features

## Usage

Setup the environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup the secret file:
```bash
echo "OPENAI_API_KEY=$(pbpaste)" > .env
```

Run the demo:
```bash
pytest *.py
```

