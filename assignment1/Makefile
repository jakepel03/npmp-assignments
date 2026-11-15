export UID := $(shell id -u)
export GID := $(shell id -g)

.PHONY: run build shell clean pdf

run: ## Start QCADesigner-E (builds the image on first run)
	docker compose run --rm qca-designer

build: ## Rebuild the image
	docker compose build

shell: ## Open a shell inside the container
	docker compose run --rm qca-designer bash

clean: ## Remove containers and the image
	docker compose down --rmi local

pdf: ## Convert one export to a cropped PDF: make pdf PS=circuits/vodilo.ps
	@test -n "$(PS)" || { echo "Usage: make pdf PS=path/to/file.ps"; exit 1; }
	docker compose run --rm qca-designer sh -c '\
		bb=$$(gs -q -dBATCH -dNOPAUSE -sDEVICE=bbox "$(PS)" 2>&1 | grep "^%%BoundingBox"); \
		grep -v "^%%HiResBoundingBox" "$(PS)" | sed "1s/.*/%!PS-Adobe-3.0 EPSF-3.0/; s/^%%BoundingBox:.*/$$bb/" | ps2pdf -dEPSCrop - "$(PS:.ps=.pdf)"'
