from PIL import Image


MAX_HEIGHT = 800


def resize_image(image_path):
    try:
        with Image.open(image_path) as image:
            image.thumbnail((image.width, MAX_HEIGHT))
            image.save(image_path)
        return True
    except Exception as e:
        print(f"Erreur lors du redimensionnement de l'image: {e}")
        return False
