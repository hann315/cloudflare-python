# Cloudflare Python

This repository contains a Python program that enables you to manage domains in Cloudflare. With this program, you can perform various operations such as updating, deleting, adding, and listing domains (and DNS Record) in your Cloudflare account.

## Installation

 It's recommended to use Python 3.6 or higher.

1. Clone the repository to your local machine:

```bash
git clone https://github.com/hann315/cloudflare-python.git
```

2. Navigate to the project directory:

```bash
cd cloudflare-python
```

3. Run the program

```bash
python cloudflare_dns_management.py
```

## Configuration

Before using the program, you need to provide your Cloudflare API credentials and configure the desired settings. Follow the steps below:

1. Obtain your Cloudflare API credentials by accessing [this page](https://dash.cloudflare.com/profile/api-tokens) in your Cloudflare account. Scroll down to API Keys tab and view Global API Key.

2. Open the `cloudflare_dns_management.py` with your favorite text editor.

3. Change line 10-11 with following value:

   - `api_key`: Your Cloudflare API key or API token.
   - `email`: Your Cloudflare account email address.

## Contributing

Contributions to this repository are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE). Feel free to modify and distribute it as needed.
