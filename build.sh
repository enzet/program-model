#!/bin/bash

mkdir -p pdf

if [ -x "$(command -v python3)" ]; then
    python3 run.py
else
    echo "No Python 3 found."
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "Images generated."
else
    echo "Images generation failed."
    exit 1
fi

if [[ `uname` == "Darwin" ]]; then
    inkscape=/Applications/Inkscape.app/Contents/Resources/bin/inkscape
elif [[ `uname` == "Linux" ]]; then
    inkscape=inkscape
fi

echo "Image converting..."

for image_name in `ls image`
do
    image_name=${image_name%.*}
    if [[ $PWD/image/${image_name}.svg -nt $PWD/pdf/${image_name}.pdf ]]; then
        ${inkscape} -z -A $PWD/pdf/${image_name}.pdf \
            $PWD/image/${image_name}.svg
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

if [[ main.tex -nt main.pdf ]]; then
    echo "TeX generation..."
    makeindex main
    bibtex main
    pdflatex -interaction=nonstopmode main
else
    echo "PDF is up to date."
fi
