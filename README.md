## Foreman REST Client Library

## Description
A REST client to handle Foreman's API. See Foreman's documentation at:

https://theforeman.org/api/1.8/

## Dependencies

### Python libraries
- requests
- json
- re

### Python version
- 3.4 (tested)

## Usage

```
from ForemanRestClient import ForemanRestClient
import getopt
import sys

username = "admin"
password = "abc123"
base_url = "https://foreman.domain.com"

foreman = ForemanRestClient.ForemanRestClient(username,password,base_url,domain='domain.com')
foreman.get_hosts()
```

## Notes

### SSL warnings

You will get an SSL warning, as we will not verify Foreman's certificate. The reason we don't do this is because this is usually a self-signed certificate (usually Puppet's self-signed certficate). The error will look something like this:
```
/usr/lib/python3/dist-packages/urllib3/connectionpool.py:794: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html
  InsecureRequestWarning)
```

You can ignore this. Perhaps we should set a flag so this can be flipped in the case you would like to verify the certificate.
