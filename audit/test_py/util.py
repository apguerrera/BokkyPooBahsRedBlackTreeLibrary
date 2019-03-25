import solcx
import rb_tree
from binarytree import build


# perform level-order traversal, the use binarytree module to print the tree
def print_contract_tree(account, contract):
    root_value = call_function(account, contract, 'root')
    if root_value == 0:
        return
    root = call_function(account, contract, 'getNode', root_value)
    queue = [root]
    items = []
    while queue:
        current_item = queue[0]
        if current_item is None:
            items.append(None)
            queue.append(None)
            queue.append(None)
        else:
            items.append(current_item)
            left = None
            right = None
            if current_item[2] != 0:
                left = call_function(account, contract, 'getNode', current_item[2])
            if current_item[3] != 0:
                right = call_function(account, contract, 'getNode', current_item[3])
            queue.append(left)
            queue.append(right)
        queue = queue[1:]
        if all((x is None for x in queue)):
            break

    for i in range(len(items)):
        if items[i] is not None:
            items[i] = items[i][0]
    print(build(items))


# in-order traversal of contract red black tree
def traverse_contract_tree(account, contract, node_value):
    node = call_function(account, contract, 'getNode', node_value)
    if node[2] != 0:
        yield from traverse_contract_tree(account, contract, node[2])

    yield node_value

    if node[3] != 0:
        yield from traverse_contract_tree(account, contract, node[3])


# convert contract red black tree to list of [3, 2, 1, 0, True]-like nodes
def contract_tree_to_list(account, contract):
    root_value = call_function(account, contract, 'root')
    if root_value != 0:
        values = list(traverse_contract_tree(account, contract, root_value))
        node_list = []
        for value in values:
            node = call_function(account, contract, 'getNode', value)
            node_list.append(node)
        return node_list
    else:
        return []


# make [3, 2, 1, 0, True] like list from local red black tree
def format_node(node):
    if node is None:
        return None
    node_list = [node.value]

    if node.parent is None or node.parent.value is None:
        node_list.append(0)
    else:
        node_list.append(node.parent.value)

    if node.left is None or node.left.value is None:
        node_list.append(0)
    else:
        node_list.append(node.left.value)

    if node.right is None or node.right.value is None:
        node_list.append(0)
    else:
        node_list.append(node.right.value)

    node_list.append(node.color == rb_tree.RED)
    return node_list


# local red black tree to list of formatted nodes
def tree_to_list(tree):
    values = list(tree)
    nodes = []
    for value in values:
        node = tree.find_node(value)
        nodes.append(format_node(node))

    return nodes


# decrypt keystore file and return account
def account_from_key(w3, key_path, passphrase):
    with open(key_path) as key_file:
        key_json = key_file.read()
    private_key = w3.eth.account.decrypt(key_json, passphrase)
    account = w3.eth.account.privateKeyToAccount(private_key)
    return account


# compile contract using solcx and return contract interface
def compile_contract(path, name):
    #solcx.set_solc_version('v0.4.25')
    compiled_contacts = solcx.compile_files([path])
    contract_interface = compiled_contacts['{}:{}'.format(path, name)]
    return contract_interface


# compile contract, deploy it from account specified, then return transaction hash and contract interface
def deploy_contract(w3, account, path, name):
    contract_interface = compile_contract(path, name)
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    transaction = contract.constructor().buildTransaction({
        'nonce': w3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    signed_transaction = w3.eth.account.signTransaction(transaction, account.privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return tx_hash.hex(), contract_interface


# return address of fresh created contract using hash returned from deploy_contract
# return None if transaction was not included to block
def created_contract_address(w3, tx_hash):
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    if not tx_receipt:
        return None
    return tx_receipt['contractAddress']


# wait for deploy transaction to be included to block, return address of created contract
def wait_contract_address(w3, tx_hash):
    w3.eth.waitForTransactionReceipt(tx_hash)
    return created_contract_address(w3, tx_hash)


# return contract object using its address and ABI
def get_contract(w3, address, abi):
    return w3.eth.contract(address=address, abi=abi)


# make transaction to contract invoking function, return transaction hash
def transact_function(w3, account, contract, function_name, args=None, add_nonce=0, gas=1000000):
    if args is not None:
        transactor = contract.functions[function_name](args)
    else:
        transactor = contract.functions[function_name]()

    transaction = transactor.buildTransaction({
        'nonce': w3.eth.getTransactionCount(account.address) + add_nonce,
        'from': account.address,
        'gas': gas
    })
    signed_transaction = w3.eth.account.signTransaction(transaction, account.privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return tx_hash.hex()


# make call to contract function, return the result of call
def call_function(account, contract, function_name, args=None):
    if args is not None:
        caller = contract.functions[function_name](args)
    else:
        caller = contract.functions[function_name]()
    return caller.call({'from': account.address})


# return event data from transaction with hash tx_hash
# return None if transaction was not included to block
def get_event(w3, contract, tx_hash, event_name):
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    if not tx_receipt:
        return None
    return contract.events[event_name]().processReceipt(tx_receipt)


# wait for transaction to be included to block, return event data
def wait_event(w3, contract, tx_hash, event_name):
    w3.eth.waitForTransactionReceipt(tx_hash)
    return get_event(w3, contract, tx_hash, event_name)
