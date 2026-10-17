# Security

## Alpha threat model

Maintainer Budget treats repository text and review comments as untrusted input.

The audit command:

- performs read-only GitHub API requests,
- does not clone or execute target repository code,
- does not run commands contained in comments,
- does not render raw HTML from comments,
- does not require write permissions.

Use a least-privilege GitHub token. For public repositories, authentication is optional but recommended for rate limits.

Please report security issues privately to the repository owner rather than opening a public issue containing exploit details.
