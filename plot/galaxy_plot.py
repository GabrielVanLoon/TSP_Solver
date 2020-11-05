import csv, numpy as np, matplotlib.pyplot as plt, click

with open('route.csv', 'r', encoding='utf-16') as file:

    reader = list(csv.DictReader(file))

    color_line = 'black'

    if click.confirm('Would you like to include a background image ?', default=True):
        img = plt.imread('galaxy_image.jpg')
        plt.imshow(img, extent=[0, 1920, 0, 1080])
        color_line = 'white'

    for row in reader:
        plt.plot([float(row['x_i']), float(row['x_j'])], [float(row['y_i']), float(row['y_j'])], '--', lw = 3, color = color_line)

    for row in reader:
        plt.plot(float(row['x_i']), float(row['y_i']), marker = '*', ms = 30, color = 'red')
    
    plt.axis('off')

    plt.show()