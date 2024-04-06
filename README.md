# roblox-group-checker

Automatically generate Roblox Groups!

**All generated groups will be placed inside of generated.txt**

## configuration

To change the length of characters to try and claim, alter the *Length* parameter in the `random_name` function inside of **main.py**

To change the refresh rate, and roblox token, edit `config.json`

### config.json values

```json
{
  "roblox-auth-token": "",
  "rate": 2
}
```

1. rate : how often to perform a group availability check.
2. roblox-auth-token : your .ROBLO-SECURITY cookie (see below)

(Getting your .ROBLO-SECURITY cookie)[https://wiki.clanny.systems/docs/roblox/getROBLOSECURITY/]
