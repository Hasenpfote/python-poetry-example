import importlib
from pathlib import Path

import pdoc

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

if __name__ == '__main__':
    here = Path(__file__).parent
    project_root_dir = here / '..'

    toml_path = project_root_dir / 'pyproject.toml'
    with open(toml_path, mode='rb') as f:
        toml_dict = tomllib.load(f)
        project = toml_dict['tool']['poetry']['name']
        module = importlib.import_module(project)
        version = toml_dict['tool']['poetry']['version']

    # Render docs
    pdoc.render.configure(
        docformat='google',
        footer_text=f'{module.__name__} {version}',
    )

    pdoc.pdoc(
        project_root_dir / 'src' / module.__name__,
        output_directory=project_root_dir / 'docs/build',
    )
