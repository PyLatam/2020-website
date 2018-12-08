import os
import click
import jinja2

import utils

config = utils.get_config()


@click.command()
@click.option('--to_dir', prompt='Target directory', default=config['project']['HTML_BUILD_PATH'])
def build_html(to_dir):
    template_path = config['project']['HTML_TEMPLATES_PATH']
    loader = jinja2.FileSystemLoader(searchpath=template_path)
    environment = jinja2.Environment(loader=loader)

    for key, name in config.items("templates"):
        template = environment.get_template(name)
        html = template.render(LANGUAGE_CODE='en')
        target_file_path = os.path.join(to_dir, name)

        with open(target_file_path, 'w') as target_file:
            target_file.write(html)

if __name__ == '__main__':
    build_html()