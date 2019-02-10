#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
from PIL import Image


class Watermarker():

    def __init__(self, original_root, watermarked_root, watermark_image_path, watermark_position):
        self.original_root = original_root
        self.watermarked_root = watermarked_root
        self.watermark_image_path = watermark_image_path
        self.watermark_position = watermark_position

        self.create_dir(self.watermarked_root)

    def create_dir(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def create_thumb(self, path, file):

        thumb_path = '%s/%s/%s' % (path.replace(self.original_root, self.watermarked_root), 'thumbs', file.replace('_', ''))
        if not os.path.exists(thumb_path):
            base_image = Image.open('%s/%s' % (path, file))
            base_image.thumbnail((500,500), Image.ANTIALIAS)
            base_image.save((thumb_path), quality=95)        

    def create_watermaked_reduced_image(self, path, file):

        watermarked_path = '%s/%s' % (path.replace(self.original_root, self.watermarked_root), file.replace('_', ''))
        if not os.path.exists(watermarked_path):
            base_image = Image.open('%s/%s' % (path, file))
            width, height = base_image.size
            watermark = Image.open(self.watermark_image_path).convert("RGBA")
            watermark_width, watermark_height = watermark.size

            if self.watermark_position == 'topleft':
                position = (0, 0)
            elif self.watermark_position == 'topright':
                position = (width - watermark_width, 0)
            elif self.watermark_position == 'bottomleft':
                position = (0, height - watermark_height)
            elif self.watermark_position == 'bottomright':
                position = (width - watermark_width, height - watermark_height)
            elif self.watermark_position == 'center':
                position = ((width - watermark_width)/2, (height - watermark_height)/2)
            elif self.watermark_position == 'bottomcenter':
                position = ((width - watermark_width)/2, height - watermark_height)
            else:
                position = (0,0)
            
            transparent = Image.new('RGBA', (width, height), (0,0,0,0))
            transparent.paste(base_image, (0,0))
            transparent.paste(watermark, position, mask=watermark)
            transparent.thumbnail((1000,1000), Image.ANTIALIAS)
            transparent.save(watermarked_path)

    def generate_watermarked_images_and_thumbs(self, path):

        self.create_dir(path)

        for root, dirs, files in os.walk(path):

            for dir in dirs:
                self.create_dir('%s/%s' % (root.replace(self.original_root, self.watermarked_root), dir))
                self.create_dir('%s/%s/%s' % (root.replace(self.original_root, self.watermarked_root), dir, 'thumbs'))
                self.generate_watermarked_images_and_thumbs('%s/%s' % (root, dir))

            for file_name in files:
                if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.png'):
                    self.create_thumb(root, file_name)
                    self.create_watermaked_reduced_image(root, file_name)


if __name__ == '__main__':
    """ example call: python watermark.py --or photos_original --wr photos/galleries --wip watermark.png --wp bottomcenter
    """

    # original_root = 'photos_original'
    # watermarked_root = ' '
    # watermark_image_path = 'watermark.png'
    # watermark_position = 'bottomcenter'

    parser = argparse.ArgumentParser()
    parser.add_argument("--or", dest="original_root", help="root of the folder containing original images")
    parser.add_argument("--wr", dest="watermarked_root", help="root of the folder to store watermarked and downsized images")
    parser.add_argument("--wip", dest="watermark_image_path", help="path to the watermark image")
    parser.add_argument("--wp", dest="watermark_position", help="position of the watermark", type=str, choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center', 'bottomcenter'])
    args = parser.parse_args()

    watermarker = Watermarker(args.original_root, args.watermarked_root, args.watermark_image_path, args.watermark_position)
    watermarker.generate_watermarked_images_and_thumbs(args.original_root)
