import argparse
import logging
import os
import subprocess


def render_card(output_path, card_template, bg_color, fg_color, caption):
    argv = [
        'convert',
        card_template,
        '-page', '+100+118',
        '-units', 'PixelsPerInch',
        '-background', bg_color,
        '-fill', fg_color,
        '-font', 'Helvetica-Neue-LT-Pro-Bold',
        '-pointsize', '4',
        '-interline-spacing', '12',
        '-density', '1200',
        '-size', '550x',
        'caption:{}'.format(caption),
        '-flatten', output_path
    ]
    subprocess.check_call(argv)


def main():
    parser = argparse.ArgumentParser(description='Generate CAH cards')
    parser.add_argument('--card_type', choices=['black', 'white'], required=True, help='CAH Card type')
    parser.add_argument('--card_template', required=True, help='Card background template .png file')
    parser.add_argument('--card_captions', required=True, help='Newline delimited file of card captions')
    parser.add_argument('--output_directory', required=True, help='Output directory for generated .png files')
    args = parser.parse_args()

    bg_color = {
        'white': 'white',
        'black': 'black'
    }[args.card_type]

    fg_color = {
        'white': 'black',
        'black': 'white'
    }[args.card_type]

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    with open(args.card_captions, 'r') as f:
        for idx, caption in enumerate(f.readlines()):
            output_path = os.path.join(args.output_directory, '_{}.png'.format(idx))
            render_card(output_path, args.card_template, bg_color, fg_color, caption.strip())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)-8s %(module)s: %(message)s")
    main()