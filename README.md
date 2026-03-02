# Py402
#### A command line tool for requesting L402-gated resources

[L402 is the standard for selling and buying digital resources. L402 allows services to charge for API endpoints in a way that is easy for AI agents to participate.](https://docs.lightning.engineering/the-lightning-network/l402)
Py402 is a command line tool that can request, pay and fetch any L402-gated resource from the web.

It is intended for demo purposes.

## Installation

`git clone https://github.com/Liongrass/Py402.git`
`cd Py402`
`python -m venv env`
`source env/bin/activate`
`pip install -r requirements.txt`

## Configuration

Optionally, you may create a `.env` configuration file and populate it with the domain of your LNbits server, as well as the admin key.

`cp .env.example .env`

## Application

To run Py402, simply execute:

`python Py402.py`

### LNbits

If you have an LNbits wallet configured, your balance will be shown, and you will be prompted to pay the invoice. Type "YES" to proceed.

Py402 will now pay the invoice, fetch the preimage and request the resource with the valid L402.

### External wallet

If you do not connect an LNbits wallet, you can still pay the invoice and submit the preimage separately, if your wallet supports this. In some wallets, this preimage may be called "payment proof" and typically looks like this: `29a2dbd5e67a29e82ed9e0895f150d0d39ee95a10da627a7c0e00a7c8f274ed9`

## Examples

Lightning Faucet provides multiple endpoints that you may use for a demonstration:

[https://lightningfaucet.com/api/l402/entropy](https://lightningfaucet.com/api/l402/entropy)

[https://lightningfaucet.com/api/l402/dad_joke](https://lightningfaucet.com/api/l402/dad_joke)

[https://lightningfaucet.com/api/l402/headers](https://lightningfaucet.com/api/l402/headers)

You may also look for suitable endpoints on [Satring](https://satring.com/)