import audit.test_py.rb_tree as rb_tree
from audit.test_py.util import *
from web3 import Web3
import random


def test_w3_connected(w3):
    print('connect to ethereum node: ', end='')

    assert w3.isConnected(), 'not connected to ethereum node'

    print('SUCCESS: ipc path: {}'.format(w3.providers[0].ipc_path))


def test_deploy(w3, account, path, name):
    print('deploy contract: ', end='')

    tx_hash, contract_interface = deploy_contract(w3, account, path, name)
    contract_address = wait_contract_address(w3, tx_hash)
    contract = get_contract(w3, contract_address, contract_interface['abi'])
    assert w3.isAddress(contract_address), 'failed to deploy contract'

    print('SUCCESS: contract deployed at address: {}'.format(contract_address))
    return contract


def test_empty(account, contract):
    print('check that contract is initialized correctly: ', end='')

    root = call_function(account, contract, 'root')
    expected = 0
    assert root == 0, 'root should be: {}, got: {}'.format(expected, root)

    first = call_function(account, contract, 'first')
    expected = 0
    assert first == expected, 'first should be: {}, got: {}'.format(expected, first)

    last = call_function(account, contract, 'last')
    expected = 0
    assert last == expected, 'last should be: {}, got: {}'.format(expected, last)

    next_123 = call_function(account, contract, 'next', 123)
    expected = 0
    assert next_123 == expected, 'next(123) should be: {}, got: {}'.format(expected, next_123)

    prev_123 = call_function(account, contract, 'prev', 123)
    expected = 0
    assert prev_123 == expected, 'prev(123) should be: {}, got: {}'.format(expected, prev_123)

    exists_123 = call_function(account, contract, 'exists', 123)
    expected = False
    assert exists_123 == expected, 'exists(123) should be: {}, got: {}'.format(expected, exists_123)

    node_123 = call_function(account, contract, 'getNode', 123)
    expected = [0, 0, 0, 0, False]
    assert node_123 == expected, 'getNode(123) should be: {}, got: {}'.format(expected, node_123)

    parent_123 = call_function(account, contract, 'parent', 123)
    expected = 0
    assert parent_123 == expected, 'parent(123) should be: {}, got: {}'.format(expected, parent_123)

    grandparent_123 = call_function(account, contract, 'grandparent', 123)
    expected = 0
    assert grandparent_123 == expected, 'grandparent(123) should be: {}, got: {}'.format(expected, grandparent_123)

    sibling_123 = call_function(account, contract, 'sibling', 123)
    expected = 0
    assert sibling_123 == expected, 'sibling(123) should be: {}, got: {}'.format(expected, sibling_123)

    uncle_123 = call_function(account, contract, 'uncle', 123)
    expected = 0
    assert uncle_123 == expected, 'uncle(123) should be: {}, got: {}'.format(expected, uncle_123)

    print('SUCCESS')


def test_trees_equal(w3, account, contract, rbt):
    print('check that contract RBT has correct structure and values: ', end='')

    local_list = tree_to_list(rbt)
    contract_list = contract_tree_to_list(account, contract)

    assert len(local_list) == len(contract_list), \
        'number of elements should be: {}, got: {}'.format(len(local_list), len(contract_list))

    for i in range(len(local_list)):
        assert local_list[i] == contract_list[i], \
            'element should be: {}, got: {}'.format(local_list[i], contract_list[i])

    print('SUCCESS')


def test_insert(w3, account, contract, items):
    print('insert elements: {}: '.format(items), end='')

    tx_hashes = []
    for item in items:
        add_nonce = int(w3.txpool.status.pending, 16)
        tx_hash = transact_function(w3, account, contract, 'insert', item, add_nonce)
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
        assert tx_receipt['status'] == 1, 'failed to insert element {} to RBT'.format(items[i])

    if len(items) > 1:
        print('SUCCESS: minimum gas: {}, maximum gas: {}, total gas: {}, average gas: {}'
              .format(min_gas_used, max_gas_used, total_gas_used, int(total_gas_used / len(tx_hashes))))
    else:
        print('SUCCESS: gas used: {}'.format(total_gas_used))


def test_remove(w3, account, contract, items):
    print('remove elements: {}: '.format(items), end='')

    tx_hashes = []
    for item in items:
        add_nonce = int(w3.txpool.status.pending, 16)
        tx_hash = transact_function(w3, account, contract, 'remove', item, add_nonce)
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
        assert tx_receipt['status'] == 1, 'failed to remove element {} to RBT'.format(items[i])

    if len(items) > 1:
        print('SUCCESS: minimum gas: {}, maximum gas: {}, total gas: {}, average gas: {}'
              .format(min_gas_used, max_gas_used, total_gas_used, int(total_gas_used / len(tx_hashes))))
    else:
        print('SUCCESS: gas used: {}'.format(total_gas_used))


def test_duplicate(w3, account, contract, items):
    print('check that contract rejects duplicate values: {}: '.format(items), end='')

    tx_hashes = []
    for item in items:
        add_nonce = int(w3.txpool.status.pending, 16)
        tx_hash = transact_function(w3, account, contract, 'insert', item, add_nonce)
        tx_hashes.append(tx_hash)

    for i in range(len(tx_hashes)):
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hashes[i])
        assert tx_receipt['status'] == 0, 'succeeded to insert duplicate element {} to RBT'.format(items[i])

    print('SUCCESS')


def test(w3, contract_path, contract_name, account, insert_items, remove_items):
    test_w3_connected(w3)

    contract = test_deploy(w3, account, contract_path, contract_name)
    test_empty(account, contract)

    rbt = rb_tree.RedBlackTree()
    test_trees_equal(w3, account, contract, rbt)

    # insert items one by one, after each insertion check that contract has correct structure and elements
    for item in insert_items:
        test_insert(w3, account, contract, [item])
        rbt.add(item)
        test_trees_equal(w3, account, contract, rbt)

        # try to insert duplicate value, check that nothing is changed
        test_duplicate(w3, account, contract, [item])
        test_trees_equal(w3, account, contract, rbt)

    # remove items one by one, after each removal check that contract has correct structure and elements
    for item in remove_items:
        test_remove(w3, account, contract, [item])
        rbt.remove(item)

        test_trees_equal(w3, account, contract, rbt)

    # insert all items, then check that contract has correct structure and elements
    test_insert(w3, account, contract, insert_items)
    for item in insert_items:
        rbt.add(item)
    test_trees_equal(w3, account, contract, rbt)

    # try to insert duplicate values, check that nothing is changed
    test_duplicate(w3, account, contract, insert_items)
    test_trees_equal(w3, account, contract, rbt)

    # remove all items, then check that contract has correct structure and elements
    test_remove(w3, account, contract, insert_items)
    for item in insert_items:
        rbt.remove(item)
    test_trees_equal(w3, account, contract, rbt)

    print('PASS')


def test_randomized(w3, contract_path, contract_name, account, n=None):
    if n is None:
        n = random.randint(1, 20)
    insert_items = random.sample(range(1, random.randint(n+1, 2000000)), n)

    remove_items = list(insert_items)
    random.shuffle(remove_items)

    test(w3, contract_path, contract_name, account, insert_items, remove_items)


if __name__ == '__main__':
    geth_ipc_path = 'testchain/geth.ipc'
    keystore_file = 'testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e'

    rbt_contract_path = 'TestBokkyPooBahsRedBlackTreeRaw.sol'
    rbt_contract_name = 'TestBokkyPooBahsRedBlackTreeRaw'

    web3 = Web3(Web3.IPCProvider(geth_ipc_path))
    actor = account_from_key(web3, keystore_file, '')

    items_to_insert = [18, 28, 17, 32, 7, 5, 21, 14, 10, 3, 23, 16, 24, 4, 29, 8, 26, 12, 2, 22, 11, 1, 31, 19, 30, 9,
                       13, 15, 6, 20, 25, 27]
    items_to_remove = [4, 14, 25, 32, 2, 30, 16, 31, 6, 26, 18, 22, 28, 23, 12, 15, 19, 27, 7, 13, 29, 11, 3, 5, 17, 1,
                       24, 20, 9, 8, 21, 10]

    test(web3, rbt_contract_path, rbt_contract_name, actor, items_to_insert, items_to_remove)
    test_randomized(web3, rbt_contract_path, rbt_contract_name, actor, 5)
