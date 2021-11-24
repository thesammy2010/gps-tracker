def base(url: str) -> dict:
    return {
        "content": None,
        "embeds": [
            {
                "title": "Location",
                "description": "Click here",
                "url": url,
                "color": 5814783,
                "image": {
                    "url": "https://images.app.goo.gl/w2giEUuRNdHahSvb6"
                },
                "thumbnail": {
                    "url": "https://images.app.goo.gl/w2giEUuRNdHahSvb6"
                }
            }
        ],
        "username": "GPS Tracking Service",
        "avatar_url": (
            "https://media.istockphoto.com/vectors/"
            "satellite-icon-black-minimalist-icon-isolated-on-white-background-vector-id867290448"
        )
    }
