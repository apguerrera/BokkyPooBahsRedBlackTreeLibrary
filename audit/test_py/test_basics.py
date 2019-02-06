from audit.test_py.util import *
from web3 import Web3
import os


def test_w3_connected(w3):
    print('connect to ethereum node: ', end='')

    assert w3.isConnected(), 'not connected to ethereum node'

    print('SUCCESS: ipc path: {}'.format(os.path.abspath(ipc_path)))


def test_deploy(w3, account):
    print('deploy contract: ', end='')

    tx_hash, contract_interface = deploy_contract(w3, account, contract_path, contract_name)
    contract_address = wait_contract_address(w3, tx_hash)
    contract = get_contract(w3, contract_address, contract_interface['abi'])
    assert w3.isAddress(contract_address), 'failed to deploy contract'

    print('SUCCESS: contract deployed at address: {}'.format(contract_address))
    return contract


def test_empty(account, contract):
    print('make sure contract is initialized correctly: ', end='')

    root = call_function(account, contract, 'root')
    assert root == 0, 'root should be: 0'

    first = call_function(account, contract, 'first')
    assert first == 0, 'first should be 0'

    last = call_function(account, contract, 'last')
    assert last == 0, 'last should be 0'

    # next_0 = call_function(account, contract, 'next', 0)
    # assert next_0 == 0, 'next(0) should be 0'

    next_123 = call_function(account, contract, 'next', 123)
    assert next_123 == 0, 'next(123) should be 0'

    # prev_0 = call_function(account, contract, 'prev', 0)
    # assert prev_0 == 0, 'prev(0) should be 0'

    prev_123 = call_function(account, contract, 'prev', 123)
    assert prev_123 == 0, 'prev(123) should be 0'

    exists_123 = call_function(account, contract, 'exists', 123)
    assert not exists_123, 'exists(123) should be false'

    node_123 = call_function(account, contract, 'getNode', 123)
    assert node_123 == NULL_NODE, 'getNode(123) should be {}'.format(NULL_NODE)

    parent_123 = call_function(account, contract, 'parent', 123)
    assert parent_123 == 0, 'parent(123) should be 0'

    grandparent_123 = call_function(account, contract, 'grandparent', 123)
    assert grandparent_123 == 0, 'grandparent(123) should be 0'

    sibling_123 = call_function(account, contract, 'sibling', 123)
    assert sibling_123 == 0, 'sibling(123) should be 0'

    uncle_123 = call_function(account, contract, 'uncle', 123)
    assert uncle_123 == 0, 'uncle(123) should be 0'

    print('SUCCESS')


def test_insert_all(w3, account, contract, items):
    print('insert data to RBT: ', end='')

    tx_hashes = []
    for item in items:
        add_nonce = int(w3.txpool.status.pending, 16)
        tx_hash = transact_function(w3, account, contract, 'insert', 1000000, item, add_nonce)
        tx_hashes.append(tx_hash)

    min_gas_used = 100000000000
    max_gas_used = -10000000000
    total_gas_used = 0
    for i in range(len(tx_hashes)):
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hashes[i])
        gas_used = tx_receipt['gasUsed']
        min_gas_used = min(gas_used, min_gas_used)
        max_gas_used = max(gas_used, max_gas_used)
        total_gas_used += gas_used
        assert tx_receipt['status'] == 1, 'failed to add element {} to RBT'.format(items[i])

    print('SUCCESS: minimum gas: {}, maximum gas: {}, total gas: {}'.format(min_gas_used, max_gas_used,
                                                                            total_gas_used))


def test_values_all(account, contract):
    print('make sure values are assigned correctly: ', end='')

    root = call_function(account, contract, 'root')

    assert root == 18, 'root should be: {}, got: {}'.format(18, root)

    first = call_function(account, contract, 'first')
    assert first == min(insert_items), 'first should be: {}, got: {}'.format(min(insert_items), first)

    last = call_function(account, contract, 'last')
    assert last == max(insert_items), 'last should be {}, got: {}'.format(max(insert_items), last)

    next_18 = call_function(account, contract, 'next', 18)
    assert next_18 == 19, 'next(18) should be: {}, got: {}'.format(19, next_18)

    prev_18 = call_function(account, contract, 'prev', 18)
    assert prev_18 == 17, 'prev(18) should be: {}, got: {}'.format(17, prev_18)

    exists_18 = call_function(account, contract, 'exists', 18)
    assert exists_18, 'exists(18) should be true'

    print('SUCCESS')


if __name__ == '__main__':
    ipc_path = 'testchain/geth.ipc'
    keystore_file = 'testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e'

    contract_path = 'TestBokkyPooBahsRedBlackTreeRaw.sol'
    contract_name = 'TestBokkyPooBahsRedBlackTreeRaw'

    w3_instance = Web3(Web3.IPCProvider(ipc_path))
    actor = account_from_key(w3_instance, keystore_file, '')

    NULL_NODE = [0, 0, 0, 0, False]

    insert_items = [18, 28, 17, 32, 7, 5, 21, 14, 10, 3, 23, 16, 24, 4, 29, 8, 26, 12, 2, 22, 11, 1, 31, 19, 30, 9, 13,
                    15, 6, 20, 25, 27]
    remove_items = [4, 14, 25, 32, 2, 30, 16, 31, 6, 26, 18, 22, 28, 23, 12, 15, 19, 27, 7, 13, 29, 11, 3, 5, 17, 1, 24,
                    20, 9, 8, 21, 10]

    test_w3_connected(w3_instance)
    rbt_contract = test_deploy(w3_instance, actor)
    test_empty(actor, rbt_contract)
    test_insert_all(w3_instance, actor, rbt_contract, insert_items)
    test_values_all(actor, rbt_contract)

    print('PASS')
