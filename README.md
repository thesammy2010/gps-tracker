# gps-tracker

> This API allows GPS information to be stored and requested

![Tests](https://github.com/thesammy2010/gps-tracker/actions/workflows/tests.yml/badge.svg)

[![.github/workflows/lint.yml](https://github.com/thesammy2010/gps-tracker/actions/workflows/lint.yml/badge.svg)](https://github.com/thesammy2010/gps-tracker/actions/workflows/lint.yml)

[![deploy](https://github.com/thesammy2010/gps-tracker/actions/workflows/deployment.yml/badge.svg)](https://github.com/thesammy2010/gps-tracker/actions/workflows/deployment.yml)

[![Coverage Status](https://coveralls.io/repos/github/thesammy2010/gps-tracker/badge.svg)](https://coveralls.io/github/thesammy2010/gps-tracker)

#### todo
- add homepage to be displayed on GitHub
- add caching and request limiting with Redis

## Usage
### GET
Request
```http request
GET /location?device=github-example HTTP/1.1

Host: track.thesammy2010.com
Authorization: base64encode("$username:$password")
Accept: application/json
Content-Type: application/json
Connection: close
```
Response
```http request
HTTP/1.1 200 OK

Date: Fri, 03 Dec 2021 20:22:41 GMT
Server: Google Frontend
Content-Length: 292
Content-Type: application/json

{
    "accuracy": 14.789999961853027,
    "activity": "",
    "altitude": 108.70000457763672,
    "battery": 22.0,
    "device": "a355b5cfccdabe30",
    "direction": 0.0,
    "latitude": 45.1234,
    "longitude": 45.1234,
    "provider": "network",
    "speed": 0.0
}
```

### POST
Request
```http request
POST /location?device=github-example HTTP/1.1

Host: track.thesammy2010.com
Authorization: base64encode("$username:$password")
Accept: application/json
Connection: close

{
    "accuracy": 14.789999961853027,
    "activity": "",
    "altitude": 108.70000457763672,
    "battery": 22.0,
    "device": "a355b5cfccdabe30",
    "direction": 0.0,
    "latitude": 45.1234,
    "longitude": 45.1234,
    "provider": "network",
    "speed": 0.0
}
```
Response
```http request
HTTP/1.1 200 OK

Date: Fri, 03 Dec 2021 20:22:41 GMT
Server: Google Frontend
Content-Length: 42
Content-Type: application/json

{
    "request_id": "61aa7c8b56d5a62cec5450da"
}
```
