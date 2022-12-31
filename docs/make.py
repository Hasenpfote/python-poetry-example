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
        project_name = toml_dict['tool']['poetry']['name']
        module_name = toml_dict['tool']['poetry']['packages'][0]['include']
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
        footer_text=f'{project_name} {version}',
    )

    pdoc.pdoc(
        project_root_dir / 'src' / module_name,
        output_directory=project_root_dir / 'docs/build',
    )
