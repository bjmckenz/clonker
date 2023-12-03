# Clonker

A simple clonk server

## Setup

 *(Install Python)*

`pip install -r requirements.txt`

## Execution

`python clonker.py [ -d ] [ -m <dist> ] [ -t <time> ] run`

* `-d` - enable debug to stdout
* `-m` - use `<dist>` *(meters)* for "close enough" limit
* `-t` - use `<time>` *(seconds)* for "close enough" time window


## Use

1. POST to `<server>/clonk`

```json
{
    "version": "1.0.0",
    "id": "my name or id",
    "latitude": 40.000000,
    "longitude": -40.00000,
    "altitude": 0.5,
    "some other data": "banana"
}
```

* `version` represents the client protocol version and must be `1.0.0`
* JSON Body must contain an `id` key. This is used to distinguish clients.
* JSON Body MAY contain any/all keys `latitude`, `longitude`, `altitude`
  * latitude and longitude are in degrees
  * altitude is meters. Altitude can be provided by both or neither events. If it's provided by only one, it will not report a clonk.
* JSON Body may contain other keys. They will be sent to clonk-mates.


2. After the window, you'll get back a list *(JSON)* of the client clonks for clients *(clonk-mates)* who also clonked (with you) within the window.

`version` in response represents server version. Currently `1.0.0`.

```json
{
  "version": "1.0.0",
  "clonks": [
    {
      "id": "client 1",
      "latitude": 40.000002,
      "longitude": -40.0,
      "altitude": 0.5,
      "at": 1701545253.113344,
      "some other data": "banana"
    },
    {
      "id": "client 2",
      "latitude": 40.000001,
      "longitude": -40.0,
      "altitude": 1.5,
      "at": 1701545255.066371,
      "some other data": "raspberry"
    }
  ]
}
```

3. You will not be in the list.

## What's a clonk?

**Requests within a given distance and time window**

## Defaults

### **Clonk window:** 0.5 seconds

Why not make this 0.0? Potentially different latencies in opening a connnection to the server. Times are recorded by the server, not reported by the client so skew is not an issue

### **Distance between devices:** 1.0 meter

Why not make this 0.0? Inaccuracies in phone position. Locations are fuzzy.

### **Settling window:** 20 ms

*(connection and network latency, and a bit of server latency)*

# License

See [License](LICENSE.md)
