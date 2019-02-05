# idmapper
Web service to map a username to full Linux identity based on inspection of a shared filesystem

# Configuration (environment variables)

## ${HOMEPATH}

Describes the template for how to find user home directories.  The default value is `/home/%u/`
The following substitutions are available:

Substitution|Meaning
`%u`|user name or UPN (see below)
`%d`|domain (or realm), if applicable
`%D`|capitalized domain (or realm), if applicable

### Notes
1. the `${HOMEPATH}` value should always end with a `/`, as the home directory value the service returns is the directory name of the computed value; leaving the path unterminated will result in an incorrect home directory value returned to the caller
2. the service derives the identity from the ownership of the computed home path; if this ownership should be computed from a file inside the home directory, add that to `${HOMEPATH}` - e.g. `/home/%u/.bashrc` may be preferable in some cases depending on how home directory ownership is structured on the shared storage

## ${UPNPATH}

Set to `true` (case sensitive) to not discard the domain/realm from the User Principal Name (UPN); if set to `false` (default), and a username is passed in as `user@domain`, *idmapper* will reduce the username to `user` before looking for a home directory for it.  If the site uses the full UPN as the home directory name, set this to `true`

# Use

This should be containerized and deployed with a shared (or underlying) filesystem bound in to match the `${HOMEPATH}`; *idmapper* will then inspect ownership of home directories in this location and return parameters to the caller.

## Usage example

This example assumes the service is running on `http://localhost:8080`, and the intention is to get ownership for a user named `john`:

```
$ curl -s localhost:8080/map/john|jq
{
      "home": "/home/john",
      "gid": 1002,
      "uid": 1002
}
```
Replace the `john` with the actual username or UPN to query other users; note that if the home directory matching the `${HOMEPATH}` pattern doesn't exist for that user, *idmapper* returns an empty JSON payload (`{}`)

