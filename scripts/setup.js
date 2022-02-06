// get database
db = db.getSiblingDB("api")

// create user
db.createUser(
    {
        user: "user",
        pwd: "passw",
        roles: [
            {
                role: "readWrite",
                db: "api"
            }
        ],
        mechanisms: [
            "SCRAM-SHA-1"
        ]
    }
)

db.auth("user", "passw")


// insert data
db.auths.insert(
    {
        username: "username",
        salt: "73616c74",
        key: "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8", // password123
        authorised: true
    }
)
db.auths.insert(
    {
        username: "username2",
        salt: "73616c74",
        key: "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8", // password123
        authorised: false
    }
)
db.data.insert(
    {
        _id: new ObjectId("615b4e4b1ad5da6788c3ea6d"),
        id: "a35c8af83fe31e00e941be6f1193b3d5afb6639f6d7afc3e5f2070434484534a",
        latitude: "45",
        longitude: "30",
        device: "iPhone",
        accuracy: "20", // metres
        battery: "95", // percent
        speed: "2", // m/s
        direction: "12", // bearing
        altitude: "50",
        provider: "data",
        activity: "n/a",
        collectedAt: new Date(2021, 10, 4, 0, 0, 0)
    }
)
db.data.insert(
    {
        _id: new ObjectId("615b4e4b1ad5da6788c3ea6e"),
        id: "50e09373d0e1146ed58d05d70550bb279d9b9d9a760215c4278440204ddb6909",
        latitude: "0",
        longitude: "1",
        device: "Android",
        accuracy: "3", // metres
        battery: "4", // percent
        speed: "5", // m/s
        direction: "6", // bearing
        altitude: "7",
        provider: "data",
        activity: "n/a",
        collectedAt: new Date(2021, 10, 5, 0, 0, 0)
    }
)
