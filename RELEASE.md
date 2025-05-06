# NbClassic Release Process

## Overview

NbClassic can be released using either the recommended automated method with
`jupyter_releaser` or the manual process described at the end of this document.

## Using `jupyter_releaser`

The recommended way to make a release is to use
[`jupyter_releaser`](https://jupyter-releaser.readthedocs.io/en/latest/get_started/making_release_from_repo.html),
which provides GitHub Actions workflows that automate the release process.

## Versioning Flow

NbClassic follows a standard versioning flow:
1. **Development** → **Pre-release** (optional) → **Final release**
2. After each release, the version is updated to a new development version.

## Automated Release Process

To begin a release, follow this two-step process:

### Step 1: Prep Release

1. Go to the **Actions** page in GitHub
2. Select the pinned **Step 1: Prep Release** workflow
3. Click on **Run workflow**
4. Configure the workflow with these parameters:
    - **Use workflow from**: Select `Branch: main` (unless you need to use an
      updated release workflow from another branch)
    - **New Version Specifier**:
        - Enter `next` to increment the micro version
        - Or enter a specific semantic version (without the leading "v") in the
          form of "major.minor.micro" to release a new major or minor version
    - **The branch to target**: Enter `main` (unless releasing from a different
      branch)
    - **Post Version Specifier**:
        - Enter the development semantic version that the target branch should
          move to after the release
        - Format should be "major.minor.micro.devN" (typically the next micro or
          minor version with dev0, e.g., 1.8.0.dev0 or 1.8.1.dev0)
    - **PR Selection**:
        - Select **Use PRs with activity since the last stable git tag**
          (recommended)
        - Alternatively, leave it unchecked and specify a custom date or git
          reference in the **Use PRs with activity since this date or git
          reference** field
5. Click **Run workflow** to start the preparation process

### Step 2: Publish Release

Once you've reviewed and approved the outputs from Step 1, proceed to publish
the release:

1. Navigate to the **Actions** page in GitHub
2. Select the **Step 2: Publish Release** workflow
3. Click on **Run workflow**
4. Configure the workflow parameters:
    - **Use workflow from**: Select `Branch: main` (unless using an updated
      release workflow from another branch)
    - **The target branch**: Enter `main` (unless releasing from a different
      branch)
    - **The URL of the draft GitHub release**:
        - Leave blank to use the latest draft (recommended)
        - Alternatively, enter a specific draft URL if you need to use a previous
          draft
    - **Comma separated list of steps to skip**:
        - Leave blank to execute all steps (recommended)
        - Specify steps to skip only when necessary for special release scenarios
5. Click **Run workflow** to start the release publication process

### Changelog Management

The changelog is updated automatically for both pre-releases and final releases.
Final releases aggregate all the pull requests since the previous final release.
As a result, some PRs may appear multiple times (typically twice), which is
consistent with changelog practices in other Jupyter projects.

## Manual Release Process

If needed, you can create a release manually by running the following commands:

```bash
# Clean the repository
git clean -dffx

# Build the distribution packages
python -m build

# Update version numbers in the codebase
tbump <new version number>

# Install the twine package for PyPI uploads
pip install twine

# Verify the distribution packages
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## Best Practices

- Test the pre-releases making the final release when possible
- Always review the generated changelog and release notes before finalizing the
  release
- For major or minor version releases, consider adding comprehensive release
  notes with notable features and breaking changes
- Announce the release to the [Releases community
  channel](https://jupyter.zulipchat.com/#narrow/channel/407388-Releases) and
  any other relevant places after completion
