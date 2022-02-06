# Changelog
All notable changes to this project will be documented in this file.

> The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]
#### Added
- Updated tag to 1.0
- Got this working on iOS via Shortcuts: https://www.icloud.com/shortcuts/81bc54e17be84e2bb99eb92ec9d190a7
- Added `/api/v{version}` to URL path to differentiate web from API (breaking change)
- Slightly improved logging
- Better validation for `POST` requests
- Sends `appid` in `POST` requests
- Location data is now queryable with more than just `device`
- Path resolves to / when invalid path is provided
- add `pre-commit`

## [0.1.5] - 2021-12-07
#### Added
- Working version deployed on Google Cloud Run
