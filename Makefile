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

# install_package:
# 	conda install -c conda-forge $1

# all: arrange_files normalize_sizes

.PHONY: lint
lint:
	pylint pokemon_image_dataset

arrange_files:
	bash src/arrange_files.sh

# split:
# 	# identify -format '%h' /Users/jimneuendorf/Developer/pokemon-image-dataset/x/3D\ Battlers\ \[All\]/Front/001.png
# 	# convert -crop 49x49 /Users/jimneuendorf/Developer/pokemon-image-dataset/x/3D\ Battlers\ \[All\]/Front/001.png test.png
# 	bash src/split.sh

# png2jpg:
# 	convert /Users/jimneuendorf/test-0.png -background white -alpha remove -alpha off test-0.jpg
