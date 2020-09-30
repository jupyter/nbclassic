To create a release, update the version number in `nbclassic/__version__.py`, then run the following:

```
git clean -dffx
python setup.py sdist
python setup.py bdist_wheel
export script_version=`python setup.py --version 2>/dev/null`
git commit -a -m "Release $script_version"
git tag $script_version
git push --all
git push --tags
pip install twine
twine check dist/* 
twine upload dist/*
```
