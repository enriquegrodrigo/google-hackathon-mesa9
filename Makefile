install:
	uv sync
	#uv run pre-commit install

lint:
	uv run pre-commit run --all

run_adk:
	uv run adk web

share_zipped_starter:
	mv README.md README.md.bak; \
	cp README_customer_facing.md README.md; \
	zip -r hackathon_starter.zip . -x "solution_*" -x "CONTRIBUTING.md" -x "package.json" -x "pnpm-lock.yaml" -x ".git/*" -x ".venv/*" -x "*/.adk/*" -x "README.md.bak" -x "README_customer_facing.md" -x "*.pyc" -x "*/**/.DS_Store" -x ".env" -x "*/.env"
	mv README.md.bak README.md

agent_descriptions:
  # npm needs to be installed globally + pnpm install md-to-pdf, puppeteer
	@echo "Merging READMEs and generating PDF..."
	cat agent*/README.md > agent_descriptions.md
	pnpm md-to-pdf agent_descriptions.md
	@echo "agent_descriptions.pdf generated successfully."
