import pygame


class Image:
    data = {}

    def getImage(href: str):
        if href not in Image.data:
            Image.data[href] = pygame.image.load(href)
        return Image.data[href]
        # return pygame.transform.scale(Image.data[href], size)
