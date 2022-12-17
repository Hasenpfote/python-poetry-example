import importlib
import os
from pathlib import Path

import git
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

    if version == '0.0.0':
        repo_dir = project_root_dir / '.git'
        if os.path.isdir(repo_dir):
            repo = git.Repo(repo_dir)
            if repo.tags:
                tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                latest_tag = tags[-1]
                version = str(latest_tag)
                if version.startswith('v'):
                    version = version[1:]

    # Render docs
    pdoc.render.configure(
        docformat='google',
        footer_text=f'{module.__name__} {version}',
    )

    pdoc.pdoc(
        project_root_dir / 'src' / module.__name__,
        output_directory=project_root_dir / 'docs/build',
    )
