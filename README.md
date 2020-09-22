# jwt.py #

A simple cli tool to view and manipulate JWT tokens.
Still under construction.

## Example 
```bash
# decode the jwt an pretty print it on the screen
cat test.jwt | ./jwt.py --pretty 
{
    "alg": "HS256",
    "typ": "JWT"
}.{
    "iat": 1422779638,
    "loggedInAs": "admin"
}.gzSraSYS8EXBxLN_oWnFSRgCzcmJmMjLiuyu5CSpyHI


# decode the jwt replache the algorithm with none and encode the token again (does not manipulate the signature)
cat test.jwt | ./jwt.py | sed 's/"HS256"/none/g' | ./jwt.py -e
eyJhbGciOm5vbmUsInR5cCI6IkpXVCJ9.eyJsb2dnZWRJbkFzIjoiYWRtaW4iLCJpYXQiOjE0MjI3Nzk2Mzh9.gzSraSYS8EXBxLN_oWnFSRgCzcmJmMjLiuyu5CSpyHI
```
