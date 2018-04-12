#!/bin/bash

if [[ `uname` == "Darwin" ]]; then
    inkscape=/Applications/Inkscape.app/Contents/Resources/bin/inkscape
elif [[ `uname` == "Linux" ]]; then
    inkscape=inkscape
fi

echo "Image converting..."

for image_name in concrete_execution execution_branch execution_cycle
do
    if [[ $PWD/image/${image_name}.svg -nt $PWD/image/${image_name}.pdf ]]; then
        $inkscape -z -A $PWD/image/${image_name}.pdf $PWD/image/${image_name}.svg
        if [ $? -eq 0 ]; then
            echo "Image ${image_name} converted."
        else
            echo "Image ${image_name} converting failed."
            exit 1
        fi
    else
        echo "Image ${image_name} is up to date."
    fi
done

echo "TeX generation..."

bibtex main
pdflatex main

