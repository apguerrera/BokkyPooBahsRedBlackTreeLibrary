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
    expected = NULL_NODE
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


def test_insert_first(w3, account, contract, items):
    print('insert element #1 to RBT: ', end='')

    tx_hash = transact_function(w3, account, contract, 'insert', 1000000, items[0])
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    gas_used = tx_receipt['gasUsed']
    assert tx_receipt['status'] == 1, 'failed to add element {} to RBT'.format(items[0])

    print('SUCCESS: gas: {}'.format(gas_used))


def test_value_first(account, contract, items):
    print('make sure value of element #1 is assigned correctly: ', end='')

    root = call_function(account, contract, 'root')
    expected = items[0]
    assert root == expected, 'root should be: {}, got: {}'.format(expected, root)

    first = call_function(account, contract, 'first')
    expected = items[0]
    assert first == expected, 'first should be: {}, got: {}'.format(expected, first)

    last = call_function(account, contract, 'last')
    expected = items[0]
    assert last == expected, 'last should be: {}, got: {}'.format(expected, last)

    next_first = call_function(account, contract, 'next', items[0])
    expected = 0
    assert next_first == expected, 'next({}) should be: {}, got: {}'.format(items[0], expected, next_first)

    prev_first = call_function(account, contract, 'prev', items[0])
    expected = 0
    assert prev_first == expected, 'prev({}) should be: {}, got: {}'.format(items[0], expected, prev_first)

    exists_first = call_function(account, contract, 'exists', items[0])
    expected = True
    assert exists_first == expected, 'exists({}) should be: {}, got: {}'.format(items[0], expected, exists_first)

    node_first = call_function(account, contract, 'getNode', items[0])
    expected = [items[0], 0, 0, 0, False]
    assert node_first == expected, 'getNode({}) should be {}, got: {}'.format(items[0], expected, node_first)

    parent_first = call_function(account, contract, 'parent', items[0])
    expected = 0
    assert parent_first == expected, 'parent({}) should be: {}, got: {}'.format(items[0], expected, parent_first)

    grandparent_first = call_function(account, contract, 'grandparent', items[0])
    expected = 0
    assert grandparent_first == expected, \
        'grandparent({}) should be: {}, got: {}'.format(items[0], expected, grandparent_first)

    sibling_first = call_function(account, contract, 'sibling', items[0])
    expected = 0
    assert sibling_first == expected, 'sibling({}) should be: {}, got: {}'.format(items[0], expected, sibling_first)

    uncle_first = call_function(account, contract, 'uncle', items[0])
    expected = 0
    assert uncle_first == expected, 'uncle({}) should be: {}, got: {}'.format(items[0], expected, uncle_first)

    print('SUCCESS')


def test_insert_second(w3, account, contract, items):
    print('insert element #2 to RBT: ', end='')

    tx_hash = transact_function(w3, account, contract, 'insert', 1000000, items[1])
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    gas_used = tx_receipt['gasUsed']
    assert tx_receipt['status'] == 1, 'failed to add element {} to RBT'.format(items[1])

    print('SUCCESS: gas: {}'.format(gas_used))


def test_value_second(account, contract, items):
    print('make sure value of element #2 is assigned correctly: ', end='')

    root = call_function(account, contract, 'root')
    expected = items[0]
    assert root == expected, 'root should be: {}, got: {}'.format(expected, root)

    first = call_function(account, contract, 'first')
    expected = min(items[:2])
    assert first == expected, 'first should be: {}, got: {}'.format(expected, first)

    last = call_function(account, contract, 'last')
    expected = max(items[:2])
    assert last == expected, 'last should be {}, got: {}'.format(expected, last)

    next_12 = call_function(account, contract, 'next', 12)
    expected = 0
    assert next_12 == expected, 'next(12) should be: {}, got: {}'.format(expected, next_12)

    next_second = call_function(account, contract, 'next', items[1])
    expected = 0 if items[1] > items[0] else items[0]
    assert next_second == expected, 'next({}) should be: {}, got: {}'.format(items[1], expected, next_second)

    next_first = call_function(account, contract, 'next', items[1])
    expected = 0 if items[1] > items[0] else items[0]
    assert next_second == expected, 'next({}) should be: {}, got: {}'.format(items[1], expected, next_second)

    prev_second = call_function(account, contract, 'prev', items[1])
    expected = 0 if items[0] > items[1] else items[0]
    assert prev_second == expected, 'prev({}) should be: 0, got: {}'.format(items[1], expected, prev_second)

    exists_second = call_function(account, contract, 'exists', items[1])
    expected = True
    assert exists_second == expected, 'exists({}) should be: {}, got: {}'.format(items[1], expected, exists_second)

    node_second = call_function(account, contract, 'getNode', items[1])
    expected = [items[1], items[0], 0, 0, True]
    assert node_second == expected, 'getNode({}) should be {}, got: {}'.format(items[1], expected, node_second)

    parent_second = call_function(account, contract, 'parent', items[1])
    expected = items[0]
    assert parent_second == expected, 'parent({}) should be: {}, got: {}'.format(items[1], expected, parent_second)

    grandparent_second = call_function(account, contract, 'grandparent', items[1])
    expected = 0
    assert grandparent_second == expected, \
        'grandparent({}) should be: {}, got: {}'.format(items[1], expected, grandparent_second)

    sibling_second = call_function(account, contract, 'sibling', items[1])
    expected = 0
    assert sibling_second == expected, 'sibling({}) should be: {}, got: {}'.format(items[1], expected, sibling_second)

    uncle_second = call_function(account, contract, 'uncle', items[1])
    expected = 0
    assert uncle_second == expected, 'uncle({}) should be: {}, got: {}'.format(items[1], expected, uncle_second)

    print('SUCCESS')


def test_insert_third(w3, account, contract, items):
    print('insert element #3 to RBT: ', end='')

    tx_hash = transact_function(w3, account, contract, 'insert', 1000000, items[2])
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    gas_used = tx_receipt['gasUsed']
    assert tx_receipt['status'] == 1, 'failed to add element {} to RBT'.format(items[2])

    print('SUCCESS: gas: {}'.format(gas_used))


def test_value_third(account, contract, items):
    print('make sure value of element #3 is assigned correctly: ', end='')

    root = call_function(account, contract, 'root')
    expected = items[0]
    assert root == expected, 'root should be: {}, got: {}'.format(expected, root)

    first = call_function(account, contract, 'first')
    expected = min(items[:3])
    assert first == expected, 'first should be: {}, got: {}'.format(expected, first)

    last = call_function(account, contract, 'last')
    expected = max(items[:3])
    assert last == expected, 'last should be {}, got: {}'.format(expected, last)

    next_12 = call_function(account, contract, 'next', 12)
    expected = 0
    assert next_12 == expected, 'next(12) should be: {}, got: {}'.format(expected, next_12)

    next_second = call_function(account, contract, 'next', items[1])
    expected = 0 if items[1] > items[0] else items[0]
    assert next_second == expected, 'next({}) should be: {}, got: {}'.format(items[1], expected, next_second)

    prev_second = call_function(account, contract, 'prev', items[1])
    expected = 0 if items[0] > items[1] else items[0]
    assert prev_second == expected, 'prev({}) should be: 0, got: {}'.format(items[1], expected, prev_second)

    exists_second = call_function(account, contract, 'exists', items[1])
    expected = True
    assert exists_second == expected, 'exists({}) should be: {}, got: {}'.format(items[1], expected, exists_second)

    node_second = call_function(account, contract, 'getNode', items[1])
    expected = [items[1], items[0], 0, 0, True]
    assert node_second == expected, 'getNode({}) should be {}, got: {}'.format(items[1], expected, node_second)

    parent_second = call_function(account, contract, 'parent', items[1])
    expected = items[0]
    assert parent_second == expected, 'parent({}) should be: {}, got: {}'.format(items[1], expected, parent_second)

    grandparent_second = call_function(account, contract, 'grandparent', items[1])
    expected = 0
    assert grandparent_second == expected, \
        'grandparent({}) should be: {}, got: {}'.format(items[1], expected, grandparent_second)

    sibling_second = call_function(account, contract, 'sibling', items[1])
    expected = 0
    assert sibling_second == expected, 'sibling({}) should be: {}, got: {}'.format(items[1], expected, sibling_second)

    uncle_second = call_function(account, contract, 'uncle', items[1])
    expected = 0
    assert uncle_second == expected, 'uncle({}) should be: {}, got: {}'.format(items[1], expected, uncle_second)

    print('SUCCESS')


# def test_insert_all(w3, account, contract, items):
#     print('insert data to RBT: ', end='')
#
#     tx_hashes = []
#     for item in items:
#         add_nonce = int(w3.txpool.status.pending, 16)
#         tx_hash = transact_function(w3, account, contract, 'insert', 1000000, item, add_nonce)
#         tx_hashes.append(tx_hash)
#
#     min_gas_used = 100000000000
#     max_gas_used = -10000000000
#     total_gas_used = 0
#     for i in range(len(tx_hashes)):
#         tx_receipt = w3.eth.waitForTransactionReceipt(tx_hashes[i])
#         gas_used = tx_receipt['gasUsed']
#         min_gas_used = min(gas_used, min_gas_used)
#         max_gas_used = max(gas_used, max_gas_used)
#         total_gas_used += gas_used
#         assert tx_receipt['status'] == 1, 'failed to add element {} to RBT'.format(items[i])
#
#     print('SUCCESS: minimum gas: {}, maximum gas: {}, total gas: {}'.format(min_gas_used, max_gas_used,
#                                                                             total_gas_used))
#
#
# def test_values_all(account, contract, items):
#     print('make sure values are assigned correctly: ', end='')
#
#     root = call_function(account, contract, 'root')
#     assert root == 18, 'root should be: {}, got: {}'.format(18, root)
#
#     first = call_function(account, contract, 'first')
#     assert first == min(items), 'first should be: {}, got: {}'.format(min(items), first)
#
#     last = call_function(account, contract, 'last')
#     assert last == max(items), 'last should be {}, got: {}'.format(max(items), last)
#
#     next_18 = call_function(account, contract, 'next', 18)
#     assert next_18 == 19, 'next(18) should be: {}, got: {}'.format(19, next_18)
#
#     prev_18 = call_function(account, contract, 'prev', 18)
#     assert prev_18 == 17, 'prev(18) should be: {}, got: {}'.format(17, prev_18)
#
#     exists_18 = call_function(account, contract, 'exists', 18)
#     assert exists_18, 'exists(18) should be true'
#
#     print('SUCCESS')


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

    test_insert_first(w3_instance, actor, rbt_contract, insert_items)
    test_value_first(actor, rbt_contract, insert_items)

    test_insert_second(w3_instance, actor, rbt_contract, insert_items)
    test_value_second(actor, rbt_contract, insert_items)

    test_insert_third(w3_instance, actor, rbt_contract, insert_items)
    test_value_third(actor, rbt_contract, insert_items)

    # test_insert_all(w3_instance, actor, rbt_contract, insert_items[2:])
    # test_values_all(actor, rbt_contract, insert_items[2:])

    print('PASS')
