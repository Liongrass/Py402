# Modules
import json
from time import sleep
import requests

# Functions and variables
from var import lnbits_server, x_api_key

headers = {"X-Api-Key" : x_api_key, "Content-type" : "application/json"}
decode_base = "https://" + lnbits_server + "/api/v1/payments/decode"
pay_base = "https://" + lnbits_server + "/api/v1/payments"
balance_base = "https://" + lnbits_server + "/api/v1/wallet"

def decode_inv(invoice):
    params = {"data": invoice}
    decode = requests.post(decode_base, json=params, headers=headers)
    decoded = decode.json()
    global payment_hash
    payment_hash = decoded["payment_hash"]
    print(f"Total price for this resource: {decoded["amount_msat"]/1000} satoshi.")
    return payment_hash

def check_lnbits():
    global lnbits
    try:
        balance = requests.get(balance_base, headers=headers)
    except requests.exceptions.ConnectionError as e:
        print(f"Unable to connect to your wallet. Error: {e}")
        lnbits = False
        return lnbits
    balanced = balance.json()
    try:
        balanced["balance"]
    except KeyError:
        print(f"Unable to find your wallet. Error: {balanced["detail"]}")
        lnbits = False
        return lnbits
    else:
        print(f"Your wallet balance: {balanced["balance"]/1000} satoshi")
        lnbits = True
        return lnbits

def payinvoice(invoice):
    print("Paying the invoice now.")
    params = {"out": True, "bolt11": invoice}
    pay = requests.post(pay_base, json=params, headers=headers)
    #paid = "{'checking_id': 'c5fefb8c290f45994419fafcbd439f05c91a5e65da0119b1cb7b6dc097fe05ac', 'payment_hash': 'c5fefb8c290f45994419fafcbd439f05c91a5e65da0119b1cb7b6dc097fe05ac', 'wallet_id': '4735a5a828904d08976b28afbb880156', 'amount': -5000, 'fee': -5005, 'bolt11': 'lnbc50n1p56840epp5chl0hrpfpazej3qelt7t6sulqhy35hn9mgq3nvwt0dkup9l7qkkqdpaf35kw6r5de5kueeqgesh2cm9wssysetpv3jhyueqg43ksmeq9q6jqumpw3ejjcqzysxqzjcsp5glgyv3kf8t3m8xzej43qxv48pvxa9hdgvpym4dpcgd2f53tu8kus9qxpqysgq9xaynz2ry80xmrq8a0tp85j9qcry8nryyfyrnn6s600g3f7ue2k47t3hu2rsglerx9thnmvy9upuy60ygqqmrgxc4ywxezpehv0l9vqpg7jh2v', 'payment_request': 'lnbc50n1p56840epp5chl0hrpfpazej3qelt7t6sulqhy35hn9mgq3nvwt0dkup9l7qkkqdpaf35kw6r5de5kueeqgesh2cm9wssysetpv3jhyueqg43ksmeq9q6jqumpw3ejjcqzysxqzjcsp5glgyv3kf8t3m8xzej43qxv48pvxa9hdgvpym4dpcgd2f53tu8kus9qxpqysgq9xaynz2ry80xmrq8a0tp85j9qcry8nryyfyrnn6s600g3f7ue2k47t3hu2rsglerx9thnmvy9upuy60ygqqmrgxc4ywxezpehv0l9vqpg7jh2v', 'fiat_provider': None, 'status': 'pending', 'memo': 'Lightning Faucet Headers Echo (5 sats)', 'expiry': '2026-03-01T06:10:25', 'webhook': None, 'webhook_status': None, 'preimage': None, 'tag': None, 'extension': None, 'time': '2026-03-01T06:00:38.610931+00:00', 'created_at': '2026-03-01T06:00:38.610940+00:00', 'updated_at': '2026-03-01T06:00:38.611021+00:00', 'labels': [], 'extra': {}}"
    paid = pay.json()
    #print(paid)

def check_invoice(payment_hash):
    check_base = pay_base + "/" + payment_hash
    check = requests.get(check_base, headers=headers)
    checked = check.json()
    try:
        checked["preimage"]
    except KeyError:
        print("Unable to pay invoice.")
        exit()
    else:
        global preimage
        preimage = checked["preimage"]
        if checked["paid"] == True:
            print(f"Invoice successfully paid. Preimage {preimage}")
            return preimage
        else:
            print("Invoice not yet paid. Checking again in 5s")
            sleep(5)
            check_invoice(payment_hash)

def obtain_content(macaroon, invoice, preimage):
    headers = {"Authorization": f"L402 {macaroon}:{preimage}"}
    print("Fetching resource from server.")
    new_response = requests.get(resource_url, headers=headers)
    print("The server's response:\n\n")
    print(new_response.content)

if __name__ == "__main__":
    resource_url = input('Request any L402-gated resource from the command line.\nTo start, enter the Url you would like to request below,\nlike this: https://www.jokes.org/402\n\n')
    print(f"Requesting resource: {resource_url}")
    response = requests.get(resource_url)
    try:
        response.headers["WWW-Authenticate"]
    except KeyError:
        print("No L402 Found. Please try again.")
        exit()
    else:
        print("Valid L402 Found!")
        invoice = response.headers["WWW-Authenticate"].split('invoice="')[1].split('"')[0]
        macaroon = response.headers["WWW-Authenticate"].split('L402 macaroon="')[1].split('"')[0]
        #invoice = "lnbc50n1p56840epp5chl0hrpfpazej3qelt7t6sulqhy35hn9mgq3nvwt0dkup9l7qkkqdpaf35kw6r5de5kueeqgesh2cm9wssysetpv3jhyueqg43ksmeq9q6jqumpw3ejjcqzysxqzjcsp5glgyv3kf8t3m8xzej43qxv48pvxa9hdgvpym4dpcgd2f53tu8kus9qxpqysgq9xaynz2ry80xmrq8a0tp85j9qcry8nryyfyrnn6s600g3f7ue2k47t3hu2rsglerx9thnmvy9upuy60ygqqmrgxc4ywxezpehv0l9vqpg7jh2v"
        check_lnbits()
    if lnbits == True:
        decode_inv(invoice)
        confirmation = input("Would you like to pay this invoice? Type YES\n\n")
        if confirmation == "YES":
            print("Here is the Macaroon. You may need it together with the preimage in the future:")
            print(f"Maracoon: {macaroon}")
            payinvoice(invoice)
            check_invoice(payment_hash)
            obtain_content(macaroon, invoice, preimage)
            print(f"DONE!\n\n")
        else:
            print("Okay. Giving up.")
            quit()
    else:
        print(invoice)
        preimage = input("You may still pay the invoice above from another wallet and provide the preimage manually:\n")
        obtain_content(macaroon, invoice, preimage)
        print(f"DONE!\n\n")