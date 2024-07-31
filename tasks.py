import re
import subprocess
import sys
from enum import Enum
from pathlib import Path

import toml
import typer

init_version_re = r"__version__ = [\'\"](\S+)[\'\"]"
poetry_version_re = r"Bumping version from (\S+) to (\S+)"
module_version_re = r"version: [\'\"]?([^\'\"\s]+)[\'\"]?"
repo_path = Path(__file__).parent
pyproject_toml = repo_path / "pyproject.toml"
pyproject = toml.loads(pyproject_toml.read_text())
package_name = pyproject["tool"]["poetry"]["name"]
src_path = repo_path / "src"
package_path = src_path / package_name


Bookmarks = {
    "github": pyproject["tool"]["poetry"]["repository"],
    "issues": pyproject["tool"]["poetry"]["repository"] + "/issues",
    "pulls": pyproject["tool"]["poetry"]["repository"] + "/pulls",
    "actions": pyproject["tool"]["poetry"]["repository"] + "/actions",
}
Bookmark = Enum(
    "Bookmark",
    names=[(key, key) for key in Bookmarks.keys()],
    module=__name__,
)


app = typer.Typer()


@app.command()
def version(
    rule: str = typer.Argument(
        None, help="Version bump rule. [major, minor, patch, prerelease]"
    ),
    force: str = typer.Option(
        None, help="Manually set the Version of the project instead of using a rule."
    ),
    commit: bool = typer.Option(False, help="Stage and commit modified files."),
):
    """Increment package version."""

    if not rule and not force:
        print("Missing argument 'rule': [major, minor, patch, prerelease]")
        sys.exit(1)

    use_rule = rule and not force

    if use_rule:
        # Run poetry version
        result = subprocess.check_output(f"poetry version {rule}", text=True).strip()

        # Lookup versions in results
        result_match = re.search(r"Bumping version from (\S+) to (\S+)", result)
        if not result_match:
            typer.echo(f"Error: Failed to bump version:\n{result.stdout}")
            raise typer.Exit()
        version, next_version = result_match.group(1), result_match.group(2)
    else:
        version = subprocess.check_output("poetry version -s", text=True).strip()
        next_version = force

    def update_version_in(path, regex, version):
        text = path.read_text(encoding="utf8", errors="ignore")
        match = re.search(regex, text)
        if not match:
            typer.echo(f"  Failed to update {path}: version undefined")
        else:
            path.write_text(text[: match.start(1)] + version + text[match.end(1) :])
            typer.echo(f"  Updated {path.relative_to(repo_path)}!")

    # Update version strings in other locals!
    version_locations = [
        (package_path / "__init__.py", r"__version__ = [\'\"](\S+)[\'\"]"),
        (repo_path / "module.yml", r"version: [\'\"]?([^\'\"\s]+)[\'\"]?"),
        (repo_path / "README.md", r"https://img.shields.io/badge/release-(\S+)-blue"),
    ]
    if not use_rule:
        version_locations.insert(
            0, (repo_path / "pyproject.toml", r"version = [\'\"]?([^\'\"\s]+)[\'\"]?")
        )

    typer.echo(f"Changing version from {version} to {next_version}...")
    if use_rule:
        typer.echo("  Updated pyproject.toml!")

    for location, regex in version_locations:
        update_version_in(location, regex, next_version)

    if commit:
        msg = f"Release v{next_version}"
        typer.echo()
        typer.echo(f"Adding commit: {msg}")

        for location, _ in version_locations:
            subprocess.check_output("git add .")

        subprocess.check_output(f'git commit -m "{msg}"')


@app.command()
def code_quality(fix: bool = False):
    """Run code quality tools locally."""

    if not fix:
        typer.echo()
        typer.echo("ISORT: Check order of imports.")
        isort_result = subprocess.run("poetry run isort bns_assets -c")
        isort_code = isort_result.returncode
        isort_status = ("FAILED!", "PASSED!")[isort_code == 0]
        typer.echo(f"ISORT: {isort_status}")

        typer.echo()
        typer.echo("BLACK: Check code formatting.")
        black_result = subprocess.run("poetry run black bns_assets --check")
        black_code = black_result.returncode
        black_status = ("FAILED!", "PASSED!")[black_code == 0]
        typer.echo(f"BLACK: {black_status}")
    else:
        typer.echo()
        typer.echo("ISORT: Sort imports.")
        isort_result = subprocess.run("poetry run isort bns_assets")
        isort_code = isort_result.returncode
        isort_status = ("FAILED!", "DONE!")[isort_code == 0]
        typer.echo(f"ISORT: {isort_status}")

        typer.echo()
        typer.echo("BLACK: Fix code formatting.")
        black_result = subprocess.run("poetry run black bns_assets")
        black_code = black_result.returncode
        black_status = ("FAILED!", "DONE!")[black_code == 0]
        typer.echo(f"BLACK: {black_status}")

    return sys.exit(isort_code or black_code)


@app.command()
def test():
    """Run test suite."""

    result = subprocess.run(
        ["pytest", package_path / "tests", "-vv", "--cov=" + package_name]
    )
    sys.exit(result.returncode)


@app.command()
def open(bookmark: Bookmark = typer.Argument(Bookmark.github.value)):
    """Opens a project bookmark."""

    url = Bookmarks[bookmark.value]
    typer.echo(f"Opening {url} in your browser.")
    typer.launch(url)


@app.command()
def release(force: bool = typer.Option(False, help="Force release!")):
    """Triggers a release in Github."""

    version = subprocess.check_output("poetry version -s", text=True).strip()
    force_flag = ("", "--force")[force]
    subprocess.check_output(f"git tag {force_flag} v{version}")
    subprocess.check_output(f"git push -u origin HEAD {force_flag}")
    subprocess.check_output(f"git push -u origin {force_flag} --tags")


if __name__ == "__main__":
    app()
