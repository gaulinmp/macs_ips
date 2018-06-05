# IP Address tracker website thingey

Although admittedly it's not much of a website, just posts JSON.
Good enough for me though.

Put a password file called "macs_ips.password" at ~/ (or wherever your script loads), in which is just a string secret password that you pass to `secret_word` below. E.g.:

```bash
echo open_sesame >> ~/macs_ips.password

curl "http://example.com/?secret_write?comp_name=Home PC&comp_ip=10.0.0.2&secret_word=open_sesame
```

You can change the location of this password file by changing `app.config['PW_FNAME']` in [macs_ips/\_\_init\_\_.py](macs_ips/__init__.py#L15) to be whatever you want (no relative paths, but absolute paths work).


Anyway:

**Read URL:** /?secret\_word=\<YOUR PASSWORD HERE\>

**Write URL:** /?secret\_write?comp\_name=NAME&comp\_ip=0.0.0.0&secret\_word=\<YOUR PASSWORD HERE\>

Write script relies on requests (`pip install requests`).

Pretty simple.
