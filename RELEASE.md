# Making a NbClassic Release

## Using `jupyter_releaser`

The recommended way to make a release is to use [`jupyter_releaser`](https://jupyter-releaser.readthedocs.io/en/latest/get_started/making_release_from_repo.html).

### Versioning

NbClassic follows the following versioning flow: development → pre-release
(optional) → final release. After each release, the version should
be updated to a development version.

To begin a release, from the `Actions` page in GitHub, select the pinned `Step 1: Prep Release` workflow then click on `Run workflow`. The `Use workflow from` option indicates the branch where the workflow file is located, while you can specify any target brach to release from in the corresponding input option. You can use the `New Version Specifier` input to specify the release version, and use the `post_version_spec` to define the development version that the target branch should move to after the release (e.g., 1.2.0.dev0 or 1.1.1.dev0 as needed). When setting a
`post_version_spec`, the full version must be specified. For example,
1.1.1.dev0 or 1.1.1rc0 are acceptable. The term `next` as is defaulted to in the `New Version Specifier` option, will result in a patch version update.

Once the `Step 1: Prep release` workflow completes successfully and ouptus are reviewed, you can run `Step 2: Publish Release` specifying the target branch and optionally the URL of the draft PR generated in the previous prep-release step.

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
