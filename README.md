[![Python package](https://github.com/Hasenpfote/pyenv_poetry_tox_pytest_example/actions/workflows/python-package.yml/badge.svg)](https://github.com/Hasenpfote/pyenv_poetry_tox_pytest_example/actions/workflows/python-package.yml)

# pyenv + poetry + tox + pytest 環境構築例

最小限の事例を記す.

特に注釈がなければ

- 各種情報の背景は 2022年12月あたり

## 前提条件

- OS は Linux または Windows を想定
- 任意の python 環境は [pyenv](https://github.com/pyenv/pyenv) で構築  
  Windows の場合は [pyenv-win](https://github.com/pyenv-win/pyenv-win) で代替
- 仮想環境は [poetry](https://github.com/python-poetry/poetry) で構築  
  グループ機能が便利なのでバージョンは 1.2 以上.
- 本例では python 3.7 / 3.8 を想定  
  3.8 は現行バージョンで, 3.7 は後方互換の最小バージョンとした開発を行っている状況など.  
  **※ 3.7 未満は依存関係がカオスなので全力回避**
- テストは [tox](https://github.com/tox-dev/tox) + [pytest](https://github.com/pytest-dev/pytest)
- 面倒なことはしない

```mermaid
flowchart TD

  subgraph system
    id11(python >= 3.7)
    id12(poetry >= 1.2)

    subgraph pyenv
      id21(python = 3.7)
      id22(python = 3.8)
    end

    subgraph project
      id31(.venv)
      subgraph .tox
        id41(py37)
        id42(py38)
      end
    end
  end

  id12 .-> id11
  id12 --> |poetry run python| id31
  id12 --> |poetry run tox| .tox
  id41 .-> id21
  id31 & id42 .-> id22
```

## 基本

### 準備

#### pyenv

##### インストール

###### for Linux

- [Automatic installer](https://github.com/pyenv/pyenv#automatic-installer) を利用
- 詳細は [pyenv installer](https://github.com/pyenv/pyenv-installer)
- 環境毎の違いは [Troubleshooting / FAQ](https://github.com/pyenv/pyenv/wiki#troubleshooting--faq)

###### for Windows

選択肢が多いので [Installation](https://github.com/pyenv-win/pyenv-win#installation) からお好みで.

Chocolatey 以外は環境変数の設定が必要になるので[詳細](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md)を参考に.

#### python

##### インストール

候補を確認

```bash
$ pyenv install -l
```

とある環境での最新は 3.7.9 / 3.8.10 だったのでインストール

```bash
$ pyenv install 3.7.9
$ pyenv install 3.8.10
```

インストール済みバージョンの確認

```bash
$ pyenv versions
```

#### poetry

##### インストール

[2022/12/07] この時点での最新は 1.2.2 で [ドキュメント](https://python-poetry.org/docs/#system-requirements) より

> ## System requirements
>
> Poetry requires **Python 3.7+**. It is multi-platform and the goal is to make it work equally well on Linux, macOS and Windows.

予め**システム**に python 3.7 以上をインストール要.

**poetry を動作させるために必要であって, プロジェクトへの制約ではない.**

[Installation](https://python-poetry.org/docs/#installation) を参考にお好みで.

##### 設定

###### プロジェクト下に仮想環境を構築

設定を確認

```bash
$ poetry config --list
```

`virtualenvs.in-project = null` なら下記を一度だけ実行

```bash
$ poetry config virtualenvs.in-project true
```

もしもプロジェクト毎に有効にしたいのであれば

```bash
$ poetry config virtualenvs.in-project true --local
```

好みの問題ではあるが, 本例では全体設定としておく.

### 手順

#### 1. 新規プロジェクトを作成

任意の場所で

```bash
$ poetry new --src pyenv_poetry_tox_pytest_example
```

ディレクトリ

```bash
pyenv_poetry_tox_pytest_example
├─ pyproject.toml
├─ README.md
├─ src
│  └─ pyenv_poetry_tox_pytest_example
│      └─ __init__.py
└─tests
   └─ __init__.py
```

- [Choosing a test layout / import rules](https://docs.pytest.org/en/latest/explanation/goodpractices.html#tests-outside-application-code)
- [Packaging a python library](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)

####  2. 使用する python を指定

プロジェクトルートに移動

```bash
$ cd pyenv_poetry_tox_pytest_example
```

**以降は特に注釈がない限りはプロジェクトルートでコマンドを実行している**

使用する python を指定

```bash
$ pyenv local 3.8.10 3.7.9
```

有効になっているバージョンを確認

```bash
$ python -V
Python 3.8.10
```

本例では 3.8.10 を現行バージョンと想定している.

##### 特記事項

動作確認を行った環境では,

- ` pyenv local 3.8.10 3.7.9` なら `python -V` で`3.8.10`
- ` pyenv local 3.7.9 3.8.10` なら `python -V` で `3.7.9`

**最初に指定をしたバージョンが有効になる.**

仮想環境の構築にも影響があるので要注意.

ディレクトリ

```bash
pyenv_poetry_tox_pytest_example
├─ .python-version (New!)
├─ pyproject.toml
├─ README.md
├─ src
│  └─ pyenv_poetry_tox_pytest_example
│      └─ __init__.py
└─tests
   └─ __init__.py
```

#### 3. `pyproject.toml` でバージョンを指定

以下のように指定をしておく.

```toml
[tool.poetry.dependencies]
python = "^3.7"
```

意味は 3.7 <= python version < 4.0 と若干緩め.

依存するモジュールによっては制限を厳しくする必要もある.

#### 4. 仮想環境を構築

 3.8.10 ベースで構築.

```bash
$ poetry env use python
```

確認は

```bash
$ poetry env info
```

ディレクトリ

```bash
pyenv_poetry_tox_pytest_example
├─ .python-version
├─ pyproject.toml
├─ README.md
├─ .venv (New!)
│  └─ ...
├─ src
│  └─ pyenv_poetry_tox_pytest_example
│      └─ __init__.py
└─tests
   └─ __init__.py
```

####  5. コードを配置

適当な機能をまとめた `utils.py` と, そのテストコードを配置する.

ディレクトリ

```bash
pyenv_poetry_tox_pytest_example
├─ .python-version
├─ pyproject.toml
├─ README.md
├─ .venv
│  └─ ...
├─ src
│  └─ pyenv_poetry_tox_pytest_example
│      ├─ __init__.py
│      └─ utils.py (New!)
└─tests
   ├─ __init__.py
   └─ test_utils.py (New!)
```

#### 6. テスト環境の準備

`poetry add` でも構わないが, 本例では諸事情から `pyproject.toml` に直接記述をする.

```toml
[tool.poetry.group.dev]
optional = true

[tool.poetry.group.dev.dependencies]
tox = "^3.27.1"

[tool.poetry.group.test]
optional = true

[tool.poetry.group.test.dependencies]
pytest = "^7.2.0"

[tool.pytest.ini_options]
addopts = [
  "--import-mode=importlib",
]
pythonpath = "src"
```

- [2022/12/09] tox >= 4.0.0 で仮想環境を認識できない不具合を確認  
  Linux Mint 21 / Windows10 共に, アクティブになっている１つの環境しか認識されない.  
  本例では 3.7 が認識されずスキップされる.  
-

インストール

```bash
$ poetry install --with dev
```

インストールでエラーがでるようならロックファイルの更新で対応

```bash
$ poetry update
```

確認

```bash
$ poetry show
```

#### 7. `tox.ini` の配置

```ini
[tox]
envlist =
    py37
    py38
skipsdist = true
isolated_build = true

[testenv]
allowlist_externals =
    poetry
commands_pre =
    poetry install --with test -v
commands =
    poetry run pytest -v
```

- `py37` / `py38` は `pyenv local` で指定されたバージョンを参照する `tox` 側のキーワード.  
  もしも 3.11.x が必要なら `py311` となる.

ディレクトリ

```bash
pyenv_poetry_tox_pytest_example
├─ .python-version
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ tox.ini (New!)
├─ .venv
│  └─ ...
├─ src
│  └─ pyenv_poetry_tox_pytest_example
│      ├─ __init__.py
│      └─ utils.py
└─tests
   ├─ __init__.py
   └─ test_utils.py
```

#### 8. テストを実行

```bash
$ poetry run tox
```

**本例では python 3.7 環境でエラーが発生するようにしている.**

ディレクトリ

```bash
pyenv_poetry_tox_pytest_example
├─ .python-version
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ tox.ini
├─ .tox (New!)
│  └─ ...
├─ .venv
│  └─ ...
├─ src
│  └─ pyenv_poetry_tox_pytest_example
│      ├─ __pycache__
│      │  └─ ...
│      ├─ __init__.py
│      └─ utils.py
└─tests
   ├─ __pycache__
   │  └─ ...
   ├─ __init__.py
   └─ test_utils.py
```

### 各種ファイル

#### `pyproject.toml`

```toml
[tool.poetry]
name = "pyenv_poetry_tox_pytest_example"
version = "0.1.0"
description = ""
authors = ["name <email>"]
readme = "README.md"
packages = [{include = "pyenv_poetry_tox_pytest_example", from = "src"}]

[tool.poetry.dependencies]
python = "^3.7"

[tool.poetry.group.dev]
optional = true

[tool.poetry.group.dev.dependencies]
tox = "^3.27.1"

[tool.poetry.group.test]
optional = true

[tool.poetry.group.test.dependencies]
pytest = "^7.2.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
addopts = [
  "--import-mode=importlib",
]
pythonpath = "src"
```

#### `tox.ini`

```ini
[tox]
envlist =
    py37
    py38
skipsdist = true
isolated_build = true

[testenv]
allowlist_externals =
    poetry
commands_pre =
    poetry install --with test -v
commands =
    poetry run pytest -v
```

#### `.gitignore`

```txt
/.tox
/.venv
/.python-version
/poetry.lock

__pycache__/
```

- `.python-version` は環境次第でマイナーバージョンに大きな差があるため.
- `poetry.lock` はお好みで.

## 拡張

基本で目的は果たしているものの, 心許ないので一手間を加える場合もある.  

好みもあるので以降は optional となる.  

### 拡張 1 - linter / formatter

#### 構成

##### solution

- [black](https://github.com/psf/black)

  コードの整形に利用.

- [isort](https://github.com/PyCQA/isort)

  `import` の並び替えに利用.

- [flake8p](https://github.com/john-hen/Flake8-pyproject)

  構文チェックに利用.

  `poetry` 経由で利用するので[オリジナル](https://github.com/PyCQA/flake8)は使えない.

  [2022/12/11] [pflake8](https://github.com/csachs/pyproject-flake8) は `max-line-length` が反映されなかったので選択肢を変更した.

  79 / 88 / 120 宗派のため.

- [mypy](https://github.com/python/mypy)

  型ヒントに利用.

  取り敢えず組み込んでおき, いつでも optional から変更できるように配慮.

```mermaid
flowchart LR

  subgraph solution
    subgraph formatter
      black
      isort
      black .- isort
    end
    subgraph linter
      flake8
      mypy
    end
  end
```

##### 環境

`vscode` 環境とそれ以外を考慮しつつ, 最終的にリポジトリへのコミットで同一性を担保する方向で.

- `solution` の設定は `pyproject.toml` で一元管理
- `vscode` は `poetry` で作成した仮想環境を利用するように設定
- `tox` に確認用の環境を仕込んでおく
- [pre-commit](https://github.com/pre-commit/pre-commit) でコミットをフックする

```mermaid
flowchart LR

  subgraph tox
    id_tox(solution)
  end

  subgraph poetry
    id_poetry(solution)
  end

  subgraph vscode
    id_vscode(solution)
  end

  subgraph pre-commit
    id_pre-commit(solution)
  end

  tox .-o poetry

  id_terminal(terminal)
  id_py(*.py)
  id_repo[(repo)]
  id_git(git)

  id_terminal .-> id_git
  vscode .-> id_git

  id_terminal --> |poetry run tox solution| id_tox --> |dry-run| id_py
  id_terminal ---> |poetry run solution| id_poetry --> |run| id_py
  id_vscode --> id_py

  id_py .-o id_repo
  id_pre-commit --> id_py
  id_git .-> |git commit| pre-commit .-> id_repo
```

#### 準備

`pyproject.toml`

```toml
...
[tool.poetry.group.dev.dependencies]
black = "^22.10.0"
isort = "^5.10.1"
Flake8-pyproject = "^1.2.2"
mypy = "^0.991"
pre-commit = "^2.20.0"
tox = "^3.27.1"

...
[tool.black]
line-length = 88
skip-string-normalization = true

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "E266", "W503",]
max-complexity = 10
extend-exclude = [".venv", "dist", ".github",]

[tool.mypy]
ignore_errors = true
#disallow_untyped_defs = true
#ignore_missing_imports = true
#no_implicit_optional = true
#show_error_context = true
#show_column_numbers = true
#warn_return_any = true
#warn_unused_ignores = true
#warn_redundant_casts = true
exclude = ["dist/",]

...
```

**`mypy` を `ignore_errors = true` で実質的に無効にしているので注意.**

`tox.ini`

```ini
[tox]
envlist =
    py37
    py38
    black
    isort
    flake8
    mypy
skipsdist = true
isolated_build = true

...

[testenv:black]
deps = black
commands_pre = # nop
commands =
    poetry run black . --check --diff --color

[testenv:isort]
deps =
    isort
    colorama
commands_pre = # nop
commands =
    poetry run isort . --check --diff --color

[testenv:flake8]
deps = Flake8-pyproject
commands_pre = # nop
commands =
    poetry run flake8p .

[testenv:mypy]
deps = mypy
commands_pre = # nop
commands =
    poetry run mypy .
```

`.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: check-toml
      - id: check-yaml
      - id: end-of-file-fixer
      - id: mixed-line-ending
        args: [--fix=lf]
      - id: trailing-whitespace
        args: [--markdown-linebreak-ext=md]
  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        additional_dependencies: [Flake8-pyproject]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
```

#### 手順

- インストール

  ```bash
  $ poetry install --with dev
  ```

- `vscode` 環境以外で直接実行

  ```bash
  $ poetry run black .
  $ poetry run isort .
  $ poetry run flake8 .
  $ poetry run mypy .
  ```

- `vscode` 環境以外で tox 経由で実行

  ```bash
  $ poetry run tox black
  $ poetry run tox isort
  $ poetry run tox flake8
  $ poetry run tox mypy
  ```

- `pre-commit` を編集時に適用する

  ```bash
  $ poetry run pre-commit install
  ```

### 拡張 2 - API の文書化

ライブラリ色の強いプロジェクトでは API の文書化が必要なので, ここでは [pdoc](https://github.com/mitmproxy/pdoc) を利用した方法を示す.  

[sphinx](https://github.com/sphinx-doc/sphinx) でも大差はない.  

#### 準備

`./pyproject.toml`

```toml
...
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
pdoc = "^12.3.0"
tomli = {version = "^2.0.1", python = "<3.11"}
...
```

`./docs/make.py`

```python
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
```

宗教上の理由がある場合は下記を参照.  

[...use numpydoc or Google docstrings?](https://pdoc.dev/docs/pdoc.html#use-numpydoc-or-google-docstrings)

#### 手順

- インストール

  ```bash
  $ poetry install --with docs
  ```

- 実行

  ```bash
  $ poetry run python ./docs/make.py
  ```

### 考察

導入していない機能や言い訳.

#### 動的バージョニング

vcs を基点に動的なバージョン管理を行うには, [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) が候補.

`poetry build` 時に自動かつ一時的に `pyproject.toml` や任意のファイルのバージョンを変更をしてくれる.

## 参考

- [Simple Python Version Management: pyenv](https://github.com/pyenv/pyenv)
- [pyenv for Windows](https://github.com/pyenv-win/pyenv-win)
- [Poetry](https://python-poetry.org)
- [tox](https://github.com/tox-dev/tox)
- [pytest](https://github.com/pytest-dev/pytest)
- [black](https://github.com/psf/black)
- [isort](https://github.com/PyCQA/isort)
- [flake8p](https://github.com/john-hen/Flake8-pyproject)
- [mypy](https://github.com/python/mypy)
- [pre-commit](https://github.com/pre-commit/pre-commit)
- [pdoc](https://github.com/mitmproxy/pdoc)
