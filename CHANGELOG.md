# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - YYYY-MM-DD
### Added

### Changed

### Fixed

## [1.1.2] - 2024-12-09
### Fixed
- mapengine version in v2.2.10

## [1.1.1] - 2024-12-09
### Added
- Intro tour

### Fixed
- mapengine version in v2.2.9

## [1.1.0] - 2024-11-14
### Added
- markdown rendering
- link to changelog in docs panel
- progress bar to show simulation state
- WMS layers flurstuecke and ertragspotenzial
- layer for combined PV ground negative criteria

### Changed
- esys panel tooltip texts
- update django-mapengine to v2.0.1

### Fixed
- 404 errors for missing MVTs
- truncated tooltips
- choropleth is reactivated when revisiting status quo
- choropleth legend
- choropleth for RE share

### Changed
- improve accessibility

## [1.0.0] - 2024-05-07
### Added
- light and dark basemaps for data visualization
- coupling of duplicated map panel controls
- dependabot
- key results for wind, pv ground and pv roof settings panels
- scenario settings
- additional slider marker
- result chart arrow indicator
- feedback during simulation: results progress bar and chart placeholders

### Changed
- Adapt municipality label font size according to zoom level
- update mapengine to v1.4.1
- Update layer list and replace wind and pv ground model data from MaStR with
  data from RPG
- django-oemof to v0.18.0
- oemof.tabular to support TSAM
- map boolean values in popup templates to Ja/Nein
- pre results can be shown before simulation has finished
- scenario page and scenario parameters

### Fixed
- duplicate loading of JS modules due to missing module support in django staticfile storage
- settlement 200m layer is coupled to settlement layer (de)-activation
- basemap controls
- top wizard layout
- municipality borders and labels
- show potential layers if detail panel is open when revisiting settings menu
- popups for distilled layers
- charts for popups
- disappearing region charts
- electricity demand base set to year 2022

## [0.1.0] - 2024-03-19
### Added
- new detail settings for wind and pv
- layers from new datapackage
- Rework navbar and add dummy content for steps 1+3
- Add new challenges step
- Add legend for wind potential areas in wind detail settings

### Changed
- refactored slider.js
- keep detail panel open on slider value change

### Fixed
- distilling
