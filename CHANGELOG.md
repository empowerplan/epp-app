# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- coupling of duplicated map panel controls
- dependabot

### Changed
- Adapt municipality label font size according to zoom level

### Fixed
- duplicate loading of JS modules due to missing module support in django staticfile storage
- settlement 200m layer is coupled to settlement layer (de)-activation

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
