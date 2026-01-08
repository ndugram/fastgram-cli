# fastapi-cli

A modern CLI tool for FastAPI developers - generate SSL certificates and more.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI Version](https://img.shields.io/badge/pypi-latest-blue)

## Features

- 🔐 Generate self-signed SSL certificates
- 🚀 Fast and easy to use
- 💅 Beautiful output with Rich library
- 📦 Ready for PyPI publication

## Installation

### From Github

```bash
pip install git+https://github.com/ndugram/fastai-cli.git
```

## Usage

### Generate SSL Certificates

```bash
fastai ssl
```

This will create:
- `certs/cert.pem` - SSL certificate
- `certs/key.pem` - Private key

### Show Help

```bash
fastai help
```

## Commands

| Command | Description |
|---------|-------------|
| `ssl` | Generate self-signed SSL certificates |
| `help` | Show available commands |

## Requirements

- Python 3.10+
- OpenSSL (for certificate generation)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

## Security

For security issues, please read our [Security Policy](SECURITY.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.