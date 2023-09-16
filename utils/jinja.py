from jinja2 import Environment, FileSystemLoader


def get_template(tmpl_name: str):
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)

    tmpl = env.get_template(tmpl_name)

    return tmpl
