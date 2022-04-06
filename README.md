# BNS Python template project
A template python project that doubles as a cpenv module. Includes automated testing, code-quality checks, and automated deployment to our ShotGrid site.

The python package is managed using the `poetry` cli tool. When developing locally you can use `poetry` to install and manage dependencies for your project.

# Continuous Integration

## Testing
Tests are run automatically via github actions on push and pull requests. See the repositories actions tab or a pull request to view the test results. You can also run the tests locally using `py -m tasks test`.

## Publishing to ShotGrid
There is another github workflow set to publish this module to ShotGrid when a new tag is pushed. You may also publish to ShotGrid manually by using `cpenv publish . --to_repo=bns_shotgun`. If you haven't setup the cpenv cli tool yet, see [cpenv - Plugin and Environment Management](https://www.notion.so/brandnewschool/cpenv-Plugin-and-Environment-Management-e53792affa4f41609b37686ff4270e1a).

# Publishing a new Version
Use the `version` task to version up the package and adjust the version number in all code locations. You can use major, minor, and patch rules to specify how much the version should be incremented.

`py -m tasks version patch`

Once the version is incremented you still need to add and commit. Finally you can create a tag matching the new version number and push your changes to trigger the Test and Publish workflow on github.
