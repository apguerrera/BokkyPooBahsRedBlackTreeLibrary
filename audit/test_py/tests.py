import audit.test_py.rb_tree as rb_tree
from audit.test_py.util import *
from web3 import Web3
from os.path import abspath


def test_w3_connected(w3):
    print('connect to ethereum node: ', end='')

    assert w3.isConnected(), 'not connected to ethereum node'

    print('SUCCESS: ipc path: {}'.format(abspath(ipc_path)))


def test_deploy(w3, account):
    print('deploy contract: ', end='')

    tx_hash, contract_interface = deploy_contract(w3, account, contract_path, contract_name)
    contract_address = wait_contract_address(w3, tx_hash)
    contract = get_contract(w3, contract_address, contract_interface['abi'])
    assert w3.isAddress(contract_address), 'failed to deploy contract'

    print('SUCCESS: contract deployed at address: {}'.format(contract_address))
    return contract


def test_trees_equal(w3, account, contract, rbt):
    print('check that both RBTs have the same structure and values: ', end='')

    local_list = tree_to_list(rbt)
    contract_list = contract_tree_to_list(account, contract)

    assert len(local_list) == len(contract_list), \
        'number of elements should be: {}, got: {}'.format(len(local_list), len(contract_list))

    for i in range(len(local_list)):
        assert local_list[i] == contract_list[i], \
            'element should be: {}, got: {}'.format(local_list[i], contract_list[i])

    print('SUCCESS: trees have the same structure and elements')


if __name__ == '__main__':
    ipc_path = 'testchain/geth.ipc'
    keystore_file = 'testchain/keystore/UTC--2017-05-20T02-37-30.360937280Z--a00af22d07c87d96eeeb0ed583f8f6ac7812827e'

    contract_path = 'TestBokkyPooBahsRedBlackTreeRaw.sol'
    contract_name = 'TestBokkyPooBahsRedBlackTreeRaw'

    w3_instance = Web3(Web3.IPCProvider(ipc_path))
    actor = account_from_key(w3_instance, keystore_file, '')

    insert_items = [18, 28, 17, 32, 7, 5, 21, 14, 10, 3, 23, 16, 24, 4, 29, 8, 26, 12, 2, 22, 11, 1, 31, 19, 30, 9, 13,
                    15, 6, 20, 25, 27]
    remove_items = [4, 14, 25, 32, 2, 30, 16, 31, 6, 26, 18, 22, 28, 23, 12, 15, 19, 27, 7, 13, 29, 11, 3, 5, 17, 1, 24,
                    20, 9, 8, 21, 10]

    test_w3_connected(w3_instance)

    rbt_local = rb_tree.RedBlackTree()
    rbt_contract = test_deploy(w3_instance, actor)
    test_trees_equal(w3_instance, actor, rbt_contract, rbt_local)

    print('PASS')
