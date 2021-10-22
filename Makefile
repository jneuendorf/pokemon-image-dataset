.PHONY: main
main:
	python main.py

init_macos:
	brew install imagemagick
	@# pipenv install
	conda create -n pokemon-image-dataset --file package-list.txt

package_list:
	conda list -n pokemon-image-dataset --export > package-list.txt

.PHONY: activate
activate:
	conda activate pokemon-image-dataset

.PHONY: lint
lint:
	pylint pokemon_image_dataset
