# Changelog

<!-- <START NEW CHANGELOG ENTRY> -->

## 0.4.1

([Full Changelog](https://github.com/jupyter/nbclassic/compare/v0.4.0...ab19ce1f648c99a0cf847cf9878f1828bedbb9a8))

### Enhancements made

- Don't shim notebook if notebook<7 is available [#123](https://github.com/jupyter/nbclassic/pull/123) ([@echarles](https://github.com/echarles))

### Bugs fixed

- Relax assert for IPythonHandler in case of notebook<6 [#122](https://github.com/jupyter/nbclassic/pull/122) ([@echarles](https://github.com/echarles))

### Other merged PRs

- Fix executable name in desktop file [#119](https://github.com/jupyter/nbclassic/pull/119) ([@antonio-rojas](https://github.com/antonio-rojas))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/nbclassic/graphs/contributors?from=2022-07-02&to=2022-07-06&type=c))

[@antonio-rojas](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3Aantonio-rojas+updated%3A2022-07-02..2022-07-06&type=Issues) | [@echarles](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3Aecharles+updated%3A2022-07-02..2022-07-06&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 0.4.0

([Full Changelog](https://github.com/jupyter/nbclassic/compare/v0.3.7...b00324a5a3b20ac58e074460050c28a8bcb876bb))

### Enhancements made

- Shim to support the notebook extensions [#113](https://github.com/jupyter/nbclassic/pull/113) ([@echarles](https://github.com/echarles))
- Fix `Check Release / check_release` CI job [#102](https://github.com/jupyter/nbclassic/pull/102) ([@echarles](https://github.com/echarles))
- nbclassic to use its own static assets [#96](https://github.com/jupyter/nbclassic/pull/96) ([@echarles](https://github.com/echarles))

### Bugs fixed

- [HOT FIX] Test Selenium CI [#114](https://github.com/jupyter/nbclassic/pull/114) ([@echarles](https://github.com/echarles))
- Fix ```link_check``` CI Job [#111](https://github.com/jupyter/nbclassic/pull/111) ([@echarles](https://github.com/echarles))
- Fix ```downstream``` CI Job [#110](https://github.com/jupyter/nbclassic/pull/110) ([@echarles](https://github.com/echarles))
- Disable ```Test Minimum Version``` CI Job [#109](https://github.com/jupyter/nbclassic/pull/109) ([@echarles](https://github.com/echarles))
- Fix ```Make SDist``` CI Job by installing babel as a build dependency  [#108](https://github.com/jupyter/nbclassic/pull/108) ([@RRosio](https://github.com/RRosio))
- Exclude Services tests from ```Linux JS Tests``` Job and Separate Workflow for flaky Selenium Tests [#105](https://github.com/jupyter/nbclassic/pull/105) ([@RRosio](https://github.com/RRosio))
- CI fix for "Testing nbclassic" on macos 3.7, 3.8, 3.9, 3.10 [#104](https://github.com/jupyter/nbclassic/pull/104) ([@ericsnekbytes](https://github.com/ericsnekbytes))
- Fix part of the ```Linux JS Tests``` / Notebook and Base Test Failures in CI Job [#103](https://github.com/jupyter/nbclassic/pull/103) ([@RRosio](https://github.com/RRosio))

### Maintenance and upkeep improvements

- Add the notebook 6.4.x tests, docs and companion files (with git history) [#94](https://github.com/jupyter/nbclassic/pull/94) ([@echarles](https://github.com/echarles))
- Add the notebook static assets (with git history) [#93](https://github.com/jupyter/nbclassic/pull/93) ([@echarles](https://github.com/echarles))

### Other merged PRs

- Add post-version-spec in tool.jupyer-releaser.options [#116](https://github.com/jupyter/nbclassic/pull/116) ([@echarles](https://github.com/echarles))
- CI fix for "Testing nbclassic" on macos / pypy [#106](https://github.com/jupyter/nbclassic/pull/106) ([@ericsnekbytes](https://github.com/ericsnekbytes))
- [CI] Fix the `Docs Tests` job [#99](https://github.com/jupyter/nbclassic/pull/99) ([@echarles](https://github.com/echarles))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/nbclassic/graphs/contributors?from=2022-03-16&to=2022-07-02&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3Ablink1073+updated%3A2022-03-16..2022-07-02&type=Issues) | [@echarles](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3Aecharles+updated%3A2022-03-16..2022-07-02&type=Issues) | [@ericsnekbytes](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3Aericsnekbytes+updated%3A2022-03-16..2022-07-02&type=Issues) | [@RRosio](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3ARRosio+updated%3A2022-03-16..2022-07-02&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyter%2Fnbclassic+involves%3AZsailer+updated%3A2022-03-16..2022-07-02&type=Issues)

## 0.3.7

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/v0.3.6...30510b64239cb46ae74367b19375dbdde797341b))

### Maintenance and upkeep improvements

- Clean up packaging and CI [#91](https://github.com/jupyterlab/nbclassic/pull/91) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2022-03-02&to=2022-03-16&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ablink1073+updated%3A2022-03-02..2022-03-16&type=Issues)

## 0.3.6

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/v0.3.5...a5f3e6ecae9baf71a1057f1a98587ef59936f687))

### Maintenance and upkeep improvements

- Depend on notebook_shim package for server-side shim layer [#88](https://github.com/jupyterlab/nbclassic/pull/88) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2022-01-11&to=2022-03-02&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ajtpio+updated%3A2022-01-11..2022-03-02&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2022-01-11..2022-03-02&type=Issues)

## 0.3.5

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/v0.3.4...c3005f28ca58d5dd81c62eb1a61f30d0c31a9498))

### Bugs fixed

- ensure extension name is passed to TerminalHandler [#79](https://github.com/jupyterlab/nbclassic/pull/79) ([@minrk](https://github.com/minrk))

### Maintenance and upkeep improvements

- Clean up downstream tests [#82](https://github.com/jupyterlab/nbclassic/pull/82) ([@blink1073](https://github.com/blink1073))
- Enforce labels on PRs [#80](https://github.com/jupyterlab/nbclassic/pull/80) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-10-27&to=2022-01-11&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ablink1073+updated%3A2021-10-27..2022-01-11&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aminrk+updated%3A2021-10-27..2022-01-11&type=Issues)

## 0.3.4

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/v0.3.3...48ae58cfa2fcd1a939dfbb6b5bd8b0f0e912b024))

### Bugs fixed

- Monkeypatch IPythonHandler to find nbclassic's jinja templates [#77](https://github.com/jupyterlab/nbclassic/pull/77) ([@Zsailer](https://github.com/Zsailer))

### Maintenance and upkeep improvements

- Run JupyterLab browser tests as downstream tests [#76](https://github.com/jupyterlab/nbclassic/pull/76) ([@Zsailer](https://github.com/Zsailer))

### Other merged PRs

- add check-release workflow [#75](https://github.com/jupyterlab/nbclassic/pull/75) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-10-22&to=2021-10-27&type=c))

[@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2021-10-22..2021-10-27&type=Issues)

## 0.3.3

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/0.3.2...d32701cb76bf4d1258e5f0fda9b1eac91e697f3a))

### Maintenance and upkeep improvements

- Use Jupyter Packaging and other cleanup [#68](https://github.com/jupyterlab/nbclassic/pull/68) ([@Zsailer](https://github.com/Zsailer))

### Other merged PRs

- add missing lines to manifest [#72](https://github.com/jupyterlab/nbclassic/pull/72) ([@Zsailer](https://github.com/Zsailer))
- add changelog comments for jupyter-releaser [#70](https://github.com/jupyterlab/nbclassic/pull/70) ([@Zsailer](https://github.com/Zsailer))
- add setup.py back to enable jupyter_releaser [#69](https://github.com/jupyterlab/nbclassic/pull/69) ([@Zsailer](https://github.com/Zsailer))
- Add workflow to test JupyterLab [#67](https://github.com/jupyterlab/nbclassic/pull/67) ([@Zsailer](https://github.com/Zsailer))
- Expose classic notebook's static assets from their original endpoints [#63](https://github.com/jupyterlab/nbclassic/pull/63) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-09-17&to=2021-10-22&type=c))

[@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ameeseeksmachine+updated%3A2021-09-17..2021-10-22&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2021-09-17..2021-10-22&type=Issues)

## 0.3.2

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/0.3.1...32ff24b059573c51e1bf91c426f8fd2fe6dac665))

### Merged PRs

- ExtensionManager's link_extension changed call signature [#64](https://github.com/jupyterlab/nbclassic/pull/64) ([@athornton](https://github.com/athornton))
- Fix link to the Jupyter Notebook repo in README [#62](https://github.com/jupyterlab/nbclassic/pull/62) ([@saiwing-yeung](https://github.com/saiwing-yeung))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-05-21&to=2021-09-17&type=c))

[@athornton](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aathornton+updated%3A2021-05-21..2021-09-17&type=Issues) | [@saiwing-yeung](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Asaiwing-yeung+updated%3A2021-05-21..2021-09-17&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Awelcome+updated%3A2021-05-21..2021-09-17&type=Issues)

## 0.3.1

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/0.3.0...f1b8540eb6e7ee33c3b923454366e34adbcaad1a))

### Maintenance and upkeep improvements

- bump jupyter_server dependency to 1.8 [#58](https://github.com/jupyterlab/nbclassic/pull/58) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-05-20&to=2021-05-21&type=c))

[@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2021-05-20..2021-05-21&type=Issues)

## 0.3.0

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/0.2.8...0df2d3341205609c1a1b4e2c8fc6e8959c7e828a))

### Enhancements made

- Support creating terminal with a given name. [#52](https://github.com/jupyterlab/nbclassic/pull/52) ([@cailiang9](https://github.com/cailiang9))

### Bugs fixed

- BUG fix: correct redirection to {base_url}/edit/*. [#55](https://github.com/jupyterlab/nbclassic/pull/55) ([@cailiang9](https://github.com/cailiang9))

### Maintenance and upkeep improvements

- patch server's sorted_extensions to prioritize nbclassic [#56](https://github.com/jupyterlab/nbclassic/pull/56) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-05-11&to=2021-05-20&type=c))

[@cailiang9](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Acailiang9+updated%3A2021-05-11..2021-05-20&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Awelcome+updated%3A2021-05-11..2021-05-20&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2021-05-11..2021-05-20&type=Issues)

## 0.2.8

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/0.2.7...eabc8408210a8b4e76efec2c57b5b4f9778b1c2a))

### Merged PRs

- Remove forced sorting of extensions [#49](https://github.com/jupyterlab/nbclassic/pull/49) ([@minrk](https://github.com/minrk))
- Add Changelog [#48](https://github.com/jupyterlab/nbclassic/pull/48) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-04-08&to=2021-05-11&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ablink1073+updated%3A2021-04-08..2021-05-11&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aminrk+updated%3A2021-04-08..2021-05-11&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Awelcome+updated%3A2021-04-08..2021-05-11&type=Issues)

## 0.2.7

## Merged PRs

* Fix deprecation warning when importing jupyter_server.transutils._ [#47](https://github.com/jupyterlab/nbclassic/pull/47) ([@martinRenou](https://github.com/martinRenou))
* Add a redirect handler to open non-notebook files from the cli [#45](https://github.com/jupyterlab/nbclassic/pull/45) ([@jtpio](https://github.com/jtpio))
* Add default_url trait to NotebookApp [#42](https://github.com/jupyterlab/nbclassic/pull/42) ([@afshin](https://github.com/afshin))
* Fix GitHub Actions badge [#40](https://github.com/jupyterlab/nbclassic/pull/40) ([@jtpio](https://github.com/jtpio))
* Run jupyter nbclassic -h on CI [#29](https://github.com/jupyterlab/nbclassic/pull/29) ([@jtpio](https://github.com/jtpio))

## Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2021-01-08&to=2021-04-08&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aafshin+updated%3A2021-01-08..2021-04-08&type=Issues) | [@blink1073](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ablink1073+updated%3A2021-01-08..2021-04-08&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ajtpio+updated%3A2021-01-08..2021-04-08&type=Issues) | [@martinRenou](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AmartinRenou+updated%3A2021-01-08..2021-04-08&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Awelcome+updated%3A2021-01-08..2021-04-08&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2021-01-08..2021-04-08&type=Issues)

## 0.2.6

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/47ff8cb...917c9f7))

### Merged PRs

* Ignore some traits in shim layer [#38](https://github.com/jupyterlab/nbclassic/pull/38) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2020-12-15&to=2021-01-08&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aafshin+updated%3A2020-12-15..2021-01-08&type=Issues)

## 0.2.5

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/cf3790c...47ff8cb))

### Merged PRs

* Update jupyter_server version, update to use prefixed fixtures [#37](https://github.com/jupyterlab/nbclassic/pull/37) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2020-12-08&to=2020-12-15&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aafshin+updated%3A2020-12-08..2020-12-15&type=Issues)

## 0.2.4

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/46bb6d5...cf3790c))

### Merged PRs

* Exclude tests from dist [#36](https://github.com/jupyterlab/nbclassic/pull/36) ([@bollwyvl](https://github.com/bollwyvl))
* Update release instructions [#34](https://github.com/jupyterlab/nbclassic/pull/34) ([@jasongrout](https://github.com/jasongrout))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2020-09-29&to=2020-12-08&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Abollwyvl+updated%3A2020-09-29..2020-12-08&type=Issues) | [@jasongrout](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ajasongrout+updated%3A2020-09-29..2020-12-08&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3AZsailer+updated%3A2020-09-29..2020-12-08&type=Issues)

## 0.2.3

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/61ea2a7...46bb6d5))

### Merged PRs

* Moves terminal websocket handling back to Jupyter Server [#33](https://github.com/jupyterlab/nbclassic/pull/33) ([@jasongrout](https://github.com/jasongrout))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2020-09-29&to=2020-09-29&type=c))

[@jasongrout](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ajasongrout+updated%3A2020-09-29..2020-09-29&type=Issues)

## 0.2.2

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/cff037e...61ea2a7))

### Merged PRs

* Add terminal and editor handlers [#31](https://github.com/jupyterlab/nbclassic/pull/31) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2020-09-25&to=2020-09-29&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Aafshin+updated%3A2020-09-25..2020-09-29&type=Issues)

## 0.2.1

([Full Changelog](https://github.com/jupyterlab/nbclassic/compare/09c8756...cff037e))

### Merged PRs

* Add setupbase.py to MANIFEST.in [#28](https://github.com/jupyterlab/nbclassic/pull/28) ([@jtpio](https://github.com/jtpio))
* Add LICENSE [#27](https://github.com/jupyterlab/nbclassic/pull/27) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterlab/nbclassic/graphs/contributors?from=2020-09-18&to=2020-09-25&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyterlab%2Fnbclassic+involves%3Ajtpio+updated%3A2020-09-18..2020-09-25&type=Issues)
