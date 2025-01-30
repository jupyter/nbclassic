# Making a NbClassic Release

## Using `jupyter_releaser`

The recommended way to make a release is to use [`jupyter_releaser`](https://github.com/jupyter-server/jupyter_releaser#checklist-for-adoption).

Note that we must use manual versions since Jupyter Releaser does not
yet support "next" or "patch" when dev versions are used.

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
