import re
import subprocess
import sys
from enum import Enum
from pathlib import Path

import toml
import typer

repo_path = Path(__file__).parent
package_name = repo_path.name
package_path = repo_path / package_name
init_version_re = r'__version__ = [\'\"](\S+)[\'\"]'
poetry_version_re = r'Bumping version from (\S+) to (\S+)'
module_version_re = r'version: [\'\"]?([^\'\"\s]+)[\'\"]?'
pyproject_toml = repo_path / 'pyproject.toml'
pyproject = toml.loads(pyproject_toml.read_text())


Bookmarks = {
    'github': pyproject['tool']['poetry']['repository'],
    'issues': pyproject['tool']['poetry']['repository'] + '/issues',
    'pulls': pyproject['tool']['poetry']['repository'] + '/pulls',
    'actions': pyproject['tool']['poetry']['repository'] + '/actions',
}
Bookmark = Enum(
    'Bookmark',
    names=[(key, key) for key in Bookmarks.keys()],
    module=__name__,
)


app = typer.Typer()


@app.command()
def version(
    rule: str = typer.Argument(
        'patch',
        help='Poetry version bump rule. [major, minor, patch]'
    ),
):
    '''Increment package version.'''

    messages = []

    # Run poetry version
    result = subprocess.run(
        ['poetry', 'version', rule],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    # Lookup versions in poetry version results
    result_match = re.search(poetry_version_re, result.stdout)
    if not result_match:
        typer.echo(f'Error: Failed to bump version:\n{result.stdout}')
        raise typer.Exit()
    version, next_version = result_match.group(1), result_match.group(2)

    typer.echo(f'Bumping version from {version} to {next_version}...')
    typer.echo('  Updated pyproject.toml!')

    # Find version in __init__.py
    init_path = package_path / '__init__.py'
    init_text = init_path.read_text()
    init_match = re.search(init_version_re, init_text)
    if not init_match:
        typer.echo(f'  Failed to update {init_path}: __version__ undefined')
    else:
        # Update version in __init__.py
        init_path.write_text(
            init_text[:init_match.start(1)]
            + next_version
            + init_text[init_match.end(1):]
        )
        typer.echo(f'  Updated {init_path.relative_to(repo_path)}!')

    # Find version in module.yml
    module_path = repo_path / 'module.yml'
    module_text = module_path.read_text()
    module_match = re.search(module_version_re, module_text)
    if not module_match:
        typer.echo(f'  Failed to update {module_path}: version undefined')
    else:
        # Update version in module.yml
        module_path.write_text(
            module_text[:module_match.start(1)]
            + next_version
            + module_text[module_match.end(1):]
        )
        typer.echo(f'  Updated {module_path.relative_to(repo_path)}!')


@app.command()
def code_quality(fix: bool = False):
    '''Run code quality tools locally.'''

    if not fix:
        typer.echo()
        typer.echo('ISORT: Check order of imports.')
        isort_result = subprocess.run('poetry run isort pytemplate tests -c')
        isort_code = isort_result.returncode
        isort_status = ('FAILED!', 'PASSED!')[isort_code == 0]
        typer.echo(f'ISORT: {isort_status}')

        typer.echo()
        typer.echo('BLACK: Check code formatting.')
        black_result = subprocess.run('poetry run black pytemplate tests --check')
        black_code = black_result.returncode
        black_status = ('FAILED!', 'PASSED!')[black_code == 0]
        typer.echo(f'BLACK: {black_status}')
    else:
        typer.echo()
        typer.echo('ISORT: Sort imports.')
        isort_result = subprocess.run('poetry run isort pytemplate tests')
        isort_code = isort_result.returncode
        isort_status = ('FAILED!', 'PASSED!')[isort_code == 0]
        typer.echo(f'ISORT: {isort_status}')

        typer.echo()
        typer.echo('BLACK: Fix code formatting.')
        black_result = subprocess.run('poetry run black pytemplate tests')
        black_code = black_result.returncode
        black_status = ('FAILED!', 'PASSED!')[black_code == 0]
        typer.echo(f'BLACK: {black_status}')

    if isort_status != 0 or black_status != 0:
        return sys.exit(1)


@app.command()
def test():
    '''Run test suite.'''

    result = subprocess.run(['pytest', '-vv', '--cov=' + package_name])
    sys.exit(result.returncode)


@app.command()
def open(bookmark: Bookmark = typer.Argument(Bookmark.github.value)):
    '''Opens a project bookmark.'''

    url = Bookmarks[bookmark.value]
    typer.echo(f'Opening {url} in your browser.')
    typer.launch(url)


if __name__ == '__main__':
    app()
