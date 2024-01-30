import colorgram
rgb_colors = []
colors = colorgram.extract("hirst.jpg", 30)
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
    extracted_colors = (r, g, b)
    rgb_colors.append(extracted_colors)
print(rgb_colors)