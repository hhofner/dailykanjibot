# convert SVG files to PNG
from wand.image import Image
import os

# Path to the folder containing SVG files
root_folder = "./kanji"
output_folder = "./kanji_pngs"

# Loop through all files in the folder
for filename in os.listdir(root_folder):
	if filename.endswith(".svg"):
		svg_path = os.path.join(root_folder, filename)
		png_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
		
		# Convert SVG to PNG
		with Image(filename=svg_path) as img:
			img.format = 'png'
			img.save(filename=png_path)
			
		print(f"Converted {filename} to {png_path}")

print("All SVGs have been converted!")
