# token_balance/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from web3 import Web3
from eth_utils import to_checksum_address
from .models import Project, User

# Initialize your Web3 provider
w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))


def get_token_balance(request):

    # Define the contract ABI and contract address
    contract_address = to_checksum_address(settings.CONTRACT_ADDRESS)
    

    # Create a contract instance
    contract = w3.eth.contract(address=contract_address, abi=settings.CONTRACT_ABI)

    # Define the Ethereum wallet address of the sender
    sender_address = '0xa1D82A08F127Dc5B614e85F1CFF8214F215603c7'
    sender_private_key = '77dc2df1192a24fe5088735ca4a092c22a3e40445f86f4cba2492bbf48cbb36f'  # Keep this private

    # Define the amount of wei to send (10 wei in this case)
    amount_wei = 100

    # Prepare the transaction
    nonce = w3.eth.get_transaction_count(sender_address)
    gas_price = w3.eth.gas_price
    gas_limit = 200000  # Adjust as needed

    transaction = {
        'chainId': 11155111,  # Mainnet
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'value': amount_wei,
        'data': contract.encodeABI(fn_name='buyTokens', args=[10]),
        'to': contract_address,
    }


    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)
    
    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    # Wait for the transaction to be mined (optional)
    w3.eth.wait_for_transaction_receipt(transaction_hash)


    # Define the Ethereum wallet address to check the balance
    wallet_address = '0xa1D82A08F127Dc5B614e85F1CFF8214F215603c7'

    # Get the token balance
    token_balance = contract.functions.inversiones(wallet_address).call()
    

    context = {
        'wallet_address': wallet_address,
        'token_balance': token_balance,
    }

    return fetch_project_from_contract(request)

def project_list(request):
    projects = Project.objects.all()
    users = User.objects.filter(address=request.user.address)  # Assuming user is authenticated
    return render(request, 'project_list.html', {'projects': projects, 'users': users})

def invest(request, project_id):
    # Get the selected project
    project = Project.objects.get(pk=project_id)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to your login page

    # Get the user's Ethereum address (assuming it's stored in the user model)
    user_address = request.user.address

    # Connect to the smart contract representing the project's token
    contract_address = project.token_contract_address  # Replace with your token contract address
    contract_abi = project.token_contract_abi  # Replace with your token contract ABI
    token_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Get the user's current token balance
    try:
        user_balance = token_contract.functions.balanceOf(user_address).call()
    except Exception as e:
        # Handle any exceptions that might occur while querying the contract
        user_balance = 0

    if request.method == 'POST':
        # Assuming you have a form with an 'investment_amount' field
        investment_amount = request.POST.get('investment_amount', 0)

        # Convert the investment amount to wei (assuming the token has 18 decimals)
        investment_amount_wei = int(investment_amount) * 10**18

        # Make sure the user has enough tokens to invest
        if user_balance >= investment_amount_wei:
            # Send a transaction to the smart contract to process the investment
            try:
                transaction_hash = token_contract.functions.invest(investment_amount_wei).transact(
                    {'from': user_address}
                )
                # Wait for the transaction to be mined (you may need to implement this)
                # Update the user's balance if needed
                user_balance -= investment_amount_wei
            except Exception as e:
                # Handle transaction errors
                pass

    return render(request, 'invest.html', {'project': project, 'user_balance': user_balance})


def fetch_project_from_contract(request):
    # Connect to the ProjectsPadre contract using its address
    contract_address = to_checksum_address(settings.CONTRACT_ADDRESS)
    contract_abi = settings.CONTRACT_ABI  # Replace with the actual contract ABI
    project_hijo_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    project_owner = project_hijo_contract.functions.propietario().call()[0]
    project_contract_address = project_hijo_contract.functions.propietario().call()[1]

    # Fetch project details from the ProjectHijo contract
    name = project_hijo_contract.functions.name().call()
    symbol = project_hijo_contract.functions.symbol().call()
    description = project_hijo_contract.functions.description().call()
    photos = project_hijo_contract.functions.photos().call()
    links = project_hijo_contract.functions.links().call()
    goal = project_hijo_contract.functions.goal().call()
    totalFunds = project_hijo_contract.functions.totalFunds().call()
    actionTokensNum = project_hijo_contract.functions.actionTokensNum().call()
    tokenPrice = project_hijo_contract.functions.tokenPrice().call()
    percentage = project_hijo_contract.functions.percentage().call()
    token_balance = project_hijo_contract.functions.inversiones('0xa1D82A08F127Dc5B614e85F1CFF8214F215603c7').call()

    # Create or update a Project model instance
    project, created = Project.objects.get_or_create(
        name=name,
        symbol=symbol,
        description=description,
        photos=photos,
        links=links,
        goal=goal,
        owner_address=project_owner,
        totalFunds=totalFunds,
        actionTokensNum=actionTokensNum,
        tokenPrice=tokenPrice,
        percentage=percentage,
    )

    user, created = User.objects.get_or_create(
        address = '0xa1D82A08F127Dc5B614e85F1CFF8214F215603c7',
        balance = token_balance
    )


    return render(request, 'icoApp/project_detail.html', {'project': project,'user':user})

