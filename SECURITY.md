# Security Policy

## Supported Versions

We currently support the latest version of fastapi-cli. Please ensure you are using the most recent release.

| Version | Supported |
|---------|-----------|
| 0.1.x | ✅ Yes |
| < 0.1 | ❌ No |

## Reporting a Vulnerability

We take the security of this project seriously. If you believe you have found a security vulnerability, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue
2. Email your findings to: n7for8572@gmail.com
3. Include in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- We will acknowledge your report within 24-48 hours
- You will receive updates on our progress at least once per week
- We will keep you informed throughout the disclosure process
- Once the issue is resolved, we will credit you in our release notes (unless you prefer to remain anonymous)

## Best Practices

- Always keep your dependencies up to date
- Use the latest version of fastapi-cli
- Review generated certificates before using them in production
- Never commit private keys (`key.pem`) to version control

## Dependencies Security

This project uses the following key dependencies:
- `typer` - CLI framework
- `rich` - Terminal output

We regularly update dependencies to include security patches.