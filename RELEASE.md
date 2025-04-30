# Making a NbClassic Release

## Using `jupyter_releaser`

The recommended way to make a release is to use [`jupyter_releaser`](https://github.com/jupyter-server/jupyter_releaser#checklist-for-adoption).

### Versioning

NbClassic follows the following versioning flow: development → pre-release
(optional) → final release. After each release, the version should
be updated to a development version.

You can use the `next` input to specify the release version, and use the
`post_version_spec` to define the development version that the
main branch should move to after the release (e.g., 1.2.0.dev0 or
1.1.1.dev0 as needed). By default, leaving the `next` input option
empty will result in a patch version update. When setting a
`post_version_spec`, the full version must be specified. For example,
1.1.1.dev0 or 1.1.1rc0 are acceptable.

### Changelog

The changelog is updated for both pre-releases and final releases.
Final releases aggregate all the pull requests since the previous
final release. As a result, some PRs may appear multiple times,
likely twice, which is consistent with changelog practices in
other Jupyter projects.

## Manual Release

To create a release, run the following:

```
git clean -dffx
python -m build
tbump <new version number>
pip install twine
twine check dist/*
twine upload dist/*
```
