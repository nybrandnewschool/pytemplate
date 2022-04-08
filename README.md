<div align="center">
  
# ❤ pytemplate

**Template for creating new Python tools at Brand New School.**

[![Test status](https://github.com/nybrandnewschool/pytemplate/workflows/Test/badge.svg)](https://github.com/nybrandnewschool/pytemplate/actions)
[![ShotGrid status](https://github.com/nybrandnewschool/pytemplate/workflows/Publish%20to%20ShotGrid/badge.svg)](https://github.com/nybrandnewschool/pytemplate/actions)
[![Version](https://img.shields.io/github/v/tag/nybrandnewschool/pytemplate)](https://github.com/nybrandnewschool/pytemplate/releases)

*Developed at [Brand New School](https://brandnewschool.com).*

</div>

## Features
- Dependency management via `poetry`.
- Automated testing.
- Doubles as cpenv module with automated publishing to ShotGrid.
- Convenient tasks module to run code-quality checks and tests.

## Template Instructions
1. Create a new repository under `nybrandnewschool` using this template.
2. Title: Adjust the title in this README.
3. Badges: Replace the repository name in each badge.
4. Description: Replaced the project description above the `Features` section.
6. Remove everything below the description in the README. You may choose to include a tool preview image, a list of features, and usage your tool in your new README.
5. Adjust the metadata in pyproject.toml, module.yml, and `__init__.py` files including resetting the version number to `0.1.0`.

## Testing
Tests are run automatically via github actions on push and pull requests. See the repositories actions tab or a pull request to view the test results. You can also run the tests locally using `py -m tasks test`.

## Publishing a new Version to ShotGrid
There is another github workflow set to publish this module to ShotGrid when a new tag is pushed.

1. Use the `version` task to increment the package. Use major, minor, or patch following [semantic versioning](https://semver.org).
```
    py -m tasks version patch
```
2. Add and commit the changed files.
3. Create a tag matching the new version.
4. Push your commit and tag to trigger the Publish to ShotGrid workflow.

You may also publish to ShotGrid manually by using `cpenv publish . --to_repo=bns_shotgun`.
