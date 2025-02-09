# #!/bin/bash
# 
# # Ensure the output directory exists
# mkdir -p kanji_pngs
# 
# # Loop through all SVG files in the kanji directory
# for file in kanji/*.svg; do
# 	# Extract the filename without the path
# 	filename=$(basename "$file")
# 	
# 	# Convert SVG to PNG using cairosvg
# 	cairosvg --scale 100 "$file" -o "kanji_pngs/$filename.png"
# 	
# 	# Print a message to show progress
# 	echo "Converted $filename to PNG"
# done
# 
# echo "All SVGs have been converted!"

for file in kanji/*.svg; do
	sed -i '' "/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/a\\
<rect width=\"100%\" height=\"100%\" fill=\"#f0f0f0\"/>" "$file"
done

echo "Done"

