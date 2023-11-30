# Clonker

A simple clonk server

## Setup

*(Install Python)*

`pip install -r requirements.txt`

## Execution

`flask --app clonker run`

## Use

1. Hit `<server>/clonk/name1`
2. After the window, you'll get back a list *(JSON)* of clients who also clonked within the window.

```json
{
    "clonks_within_window": [
        {
            "at": 1701368861.977858,
            "username": "aaa"
        },
        {
            "at": 1701368863.5652878,
            "username": "bbb"
        }
    ]
}
```

*(`at` represents server time in ms)*

3. You will probably be in the list.

## Defaults

**Clonk window:** 2 seconds

**Settling window:** 20 ms
*(This compensates for server latency, not network latency)*

# License

See [License](LICENSE.md)
