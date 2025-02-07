import requests

API_URL = "https://bazcoin.org:5000"

def create_wallet():
    password = input("Enter a password for your new wallet: ")
    response = requests.post(f"{API_URL}/wallet/create", json={'password': password})

    if response.status_code == 201:
        data = response.json()
        print(f"Wallet created! Wallet ID: {data['wallet_id']}, Balance: {data['balance']} BAZC")
        return data['wallet_id'], password
    else:
        print(f"Error: {response.json().get('error')}")
        return None, None

def use_existing_wallet():
    wallet_id = input("Enter your wallet ID: ")
    password = input("Enter your wallet password: ")
    response = requests.get(f'{API_URL}/wallet/balance?wallet_id={wallet_id}')

    if response.status_code == 200:
        print("Wallet found and ready to use.")
        return wallet_id, password
    else:
        print("Wallet not found or incorrect credentials.")
        return None, None

def check_balance(wallet_id):
    response = requests.get(f'{API_URL}/wallet/balance?wallet_id={wallet_id}')

    if response.status_code == 200:
        data = response.json()
        print(f"Wallet ID: {data['wallet_id']}, Balance: {data['balance']} BAZC")
    else:
        print(f"Error: {response.json().get('error')}")

def make_transaction(sender_id, password):
    receiver = input("Enter the receiver's wallet ID: ")
    amount = float(input("Enter the amount to send: "))

    response = requests.post(f'{API_URL}/transactions/new', json={
        'sender': sender_id,
        'receiver': receiver,
        'amount': amount,
        'password': password
    })

    if response.status_code == 201:
        data = response.json()
        print(f"{data['message']}, txid: {data['txid']}")
    else:
        print(f"Error: {response.json().get('error')}")

def change_password(wallet_id, old_password):
    new_password = input("Enter your new password: ")

    response = requests.post(f'{API_URL}/wallet/change_password', json={
        'wallet_id': wallet_id,
        'old_password': old_password,
        'new_password': new_password
    })

    if response.status_code == 200:
        print("Password updated successfully!")
        return new_password
    else:
        print(f"Error: {response.json().get('error')}")
        return old_password

def get_transaction():
    txid = input("Enter txid : ")
    response = requests.get(f'{API_URL}/transaction/get?txid={txid}')

    if response.status_code == 200:
        data = response.json()
        data = data['transaction']
        print(f"ID: {data['id']}\nSender: {data['sender']}\nReceiver: {data['receiver']}\nAmount: {data['amount']}\nFee: {data['fee']}\ntxid: {data['txid']}\nConfirmations: {data['confirmations']}\n")
    else:
        print(f"Error: {response.json().get('error')}")

def main():
    print("Welcome to BAZCOIN CLI!")
    wallet_id, password = None, None

    while True:
        print("\nMenu:")
        print("1. Create Wallet")
        print("2. Use Existing Wallet")
        print("3. Check Balance")
        print("4. Make Transaction")
        print("5. Change Password")
        print("6. Get Transaction")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            wallet_id, password = create_wallet()
        elif choice == "2":
            wallet_id, password = use_existing_wallet()
        elif choice == "3":
            if wallet_id:
                check_balance(wallet_id)
            else:
                print("Please create or select a wallet first.")
        elif choice == "4":
            if wallet_id and password:
                make_transaction(wallet_id, password)
            else:
                print("Please create or select a wallet first.")
        elif choice == "5":
            if wallet_id and password:
                password = change_password(wallet_id, password)
            else:
                print("Please create or select a wallet first.")
        elif choice == "6":
            get_transaction()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
