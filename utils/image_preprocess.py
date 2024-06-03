from PIL import Image
import cv2
import numpy as np
from typing import Union
from pathlib import Path

import supervision as sv


class ImagePreprocess:
    def __init__(self) -> None:
        self.masked_images = []

    def reset(self):
        self.masked_images = []

    def get_masked_image(self, image: np.ndarray, detections: sv.Detections) -> None:

        for idx in range(len(detections.class_id)):
            mask = detections.mask[idx].astype(np.uint8)*255

            masked_image = cv2.bitwise_and(
                image, image, mask=mask
            )

            masked_image = self.flatten(masked_image, mask)

            # cv2.imwrite(f'./test_{idx}_b.jpg', masked_image)

            masked_image = self.opencv2pil(masked_image)
            masked_image = self.make_square(masked_image)

            # masked_image.save(f'./test_{idx}.jpg', quality=100)

            self.masked_images.append(masked_image)

    def get_masked_image_no_detections(self, image: np.ndarray, masks: np.ndarray) -> None:

        for idx, mask in enumerate(masks):
            mask = mask.astype(np.uint8)*255

            masked_image = cv2.bitwise_and(
                image, image, mask=mask
            )

            # masked_image = self.flatten(masked_image, mask)
            masked_image = self.find_box(masked_image, mask)

            # cv2.imwrite(f'./test_{idx}_b.jpg', masked_image)

            masked_image = self.opencv2pil(masked_image)
            masked_image = self.make_square(masked_image)

            # masked_image.save(f'./test_{idx}.jpg', quality=100)

            self.masked_images.append(masked_image)

    def save(self, image: Union[Image.Image, np.ndarray], path="./", name="image") -> None:
        path = Path(path)

        try:
            if isinstance(image, Image.Image):
                image.save((path / f'{name}.jpg'), quality=100)

            if isinstance(image, np.ndarray):
                cv2.imwrite(str(path / f'{name}.jpg'), image)

        except Exception as e:
            print(e)

    def resize(self, image: np.ndarray, isMask=False):
        h, w = image.shape[:2]
        k = max(h, w)

        size = (k, k) if isMask else (k, k, 3)
        new_img = np.zeros(size, np.uint8)

        new_img[(k-h)//2:(k-h)//2 + h, (k-w)//2:(k-w)//2 + w] = image

        image = None

        return new_img

    def flatten(self, image: np.ndarray, mask: np.ndarray):
        image = self.resize(image)
        mask = self.resize(mask, isMask=True)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            1
        )
        contours = contours[-1]

        rect = cv2.minAreaRect(contours)

        del contours

        # (h, w), angle, scale
        M = cv2.getRotationMatrix2D(
            (image.shape[1]/2, image.shape[0]/2),
            rect[2],
            1.0
        )

        img_rot = cv2.warpAffine(
            image,
            M,
            (image.shape[1], image.shape[0])
        )

        # rotate bounding box
        box = cv2.boxPoints(rect)
        pts = np.intp(cv2.transform(np.array([box]), M))[0]
        pts[pts < 0] = 0

        # crop
        image = img_rot[pts[1][1]:pts[0][1],
                        pts[1][0]:pts[2][0]]

        if rect[1][0] < rect[1][1]:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

        del img_rot

        return image

    def find_box(self, image: np.ndarray, mask: np.ndarray):
        x, y, w, h = cv2.boundingRect(mask)

        return image[y:y+h, x:x+w]

    def make_square(self, image: Image.Image, size=320, fill_color=(0, 0, 0)) -> Image.Image:
        base = Image.new('RGB', (size, size), fill_color)
        x, y = image.size
        ratio = size / max(x, y)
        image = image.resize((int(x * ratio), int(y * ratio)))
        base.paste(image, (int((size-image.width) / 2),
                           int((size-image.height) / 2)))

        image.close()

        return base

    def pil2opencv(self, image: Image.Image) -> np.ndarray:
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image

    def opencv2pil(self, image: np.ndarray) -> Image.Image:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return image
