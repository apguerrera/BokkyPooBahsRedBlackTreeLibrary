# AddressStatus

Source file [../../chain/contracts/AddressStatus.sol](../../chain/contracts/AddressStatus.sol).

<br />

<hr />

```javascript
// AG Ok
pragma solidity ^0.4.25;

// ----------------------------------------------------------------------------
// BokkyPooBah's Red-Black Tree Library v0.90
//
// A Solidity Red-Black Tree library to store and access a sorted list of
// unsigned integer data in a binary search tree.
// The Red-Black algorithm rebalances the binary search tree, resulting in
// O(log n) insert, remove and search time (and ~gas)
//
// https://github.com/bokkypoobah/BokkyPooBahsRedBlackTreeLibrary
//
//
// Enjoy. (c) BokkyPooBah / Bok Consulting Pty Ltd 2018. The MIT Licence.
// ----------------------------------------------------------------------------

// AG Ok
library BokkyPooBahsRedBlackTreeLibrary {
    // AG Ok
    struct Node {
        // AG - Next 4 Ok
        uint parent;
        uint left;
        uint right;
        bool red;
    }
    // AG Ok
    struct Tree {
        // AG Ok
        uint root;
        // AG Ok
        mapping(uint => Node) nodes;
        // AG - Next 3 Ok
        bool initialised;
        uint inserted;
        uint removed;
    }

    // AG Ok - Sentinel can be set to non null if 0 is a required key  
    // AG T: Set sentinel to various numbers
    uint private constant SENTINEL = 0;
    // AG Ok
    event Log(string where, string action, uint key, uint parent, uint left, uint right, bool red);
    // AG Ok
    function init(Tree storage self) internal {
        // AG Ok
        require(!self.initialised);
        // AG Ok  
        self.root = SENTINEL;
        // AG Ok - Setting nodes[0] to an empty root
        self.nodes[SENTINEL] = Node(SENTINEL, SENTINEL, SENTINEL, false);
        // AG Ok
        self.initialised = true;
    }
    // AG Ok - T: check inserting into the tree to get a false count  
    function count(Tree storage self) internal view returns (uint _count) {
        // AG Ok
        return self.inserted >= self.removed ? self.inserted - self.removed: 0;
    }
    // AG Ok - T: various inserts but add a first and last check which should pass
    function first(Tree storage self) internal view returns (uint _key) {
        // AG Ok
        _key = self.root;
        // AG Ok
        while (_key != SENTINEL && self.nodes[_key].left != SENTINEL) {
            // AG Ok
            _key = self.nodes[_key].left;
        }
    }
    // AG Ok - Symmetrical to first()
    function last(Tree storage self) internal view returns (uint _key) {
        // AG Ok
        _key = self.root;
        // AG Ok - T: Can nodes be inserted with non null .right?
        while (_key != SENTINEL && self.nodes[_key].right != SENTINEL) {
            // AG Ok
            _key = self.nodes[_key].right;
        }
    }
    // AG Ok
    function next(Tree storage self, uint x) internal view returns (uint y) {
        // AG Ok
        require(x != SENTINEL);
        // AG Ok - Next node
        if (self.nodes[x].right != SENTINEL) {
            // AG - To Check min
            y = treeMinimum(self, self.nodes[x].right);
        // AG Ok
        } else {
            // AG OK - Up the tree
            y = self.nodes[x].parent;
            // AG OK - Progress up the tree until it diverges to the next node
            while (y != SENTINEL && x == self.nodes[y].right) {
                // AG Ok
                x = y;
                // AG Ok
                y = self.nodes[y].parent;
            }
        }
        // AG Ok - Does it need to be explicit?
        return y;
    }
    // AG Ok - Symmetrical to next()
    function prev(Tree storage self, uint x) internal view returns (uint y) {
        // AG Ok
        require(x != SENTINEL);
        // AG Ok
        if (self.nodes[x].left != SENTINEL) {
            // AG Ok
            y = treeMaximum(self, self.nodes[x].left);
        // AG Ok
        } else {
            // AG Ok
            y = self.nodes[x].parent;
            // AG Ok
            while (y != SENTINEL && x == self.nodes[y].left) {
                // AG Ok
                x = y;
                // AG Ok
                y = self.nodes[y].parent;
            }
        }
        // AG Ok
        return y;
    }
    // AG Ok - Search for key in tree, return bool
    function exists(Tree storage self, uint key) internal view returns (bool _exists) {
        // AG Ok
        require(key != SENTINEL);
        // AG Ok
        uint _key = self.root;
        // AG Ok - T: If adding the if into the while condition helps
        while (_key != SENTINEL) {
            // AG Ok
            if (key == _key) {
                // AG Ok
                _exists = true;
                // AG Ok
                return;
            }
            // AG Ok
            if (key < _key) {
                // AG Ok
                _key = self.nodes[_key].left;
            // AG Ok
            } else {
                // AG Ok
                _key = self.nodes[_key].right;
            }
        }
    }
    // AG Ok
    function getNode(Tree storage self, uint key) internal view returns (uint _returnKey, uint _parent, uint _left, uint _right, bool _red) {
        // AG Ok
        require(key != SENTINEL);
        // AG Ok
        uint _key = self.root;
        // AG Ok
        while (_key != SENTINEL) {
            // AG Ok - Might want to put the if equals statement sequential and last to save gas
            if (key == _key) {
                // AG Ok - T: Check memory
                Node memory node = self.nodes[key];
                // AG Ok
                return (key, node.parent, node.left, node.right, node.red);
            }
            // AG Ok
            if (key < _key) {
                // AG Ok
                _key = self.nodes[_key].left;
            // AG Ok
            } else {
                // AG Ok
                _key = self.nodes[_key].right;
            }
        }
        // AG Ok - Return empty node
        return (SENTINEL, SENTINEL, SENTINEL, SENTINEL, false);
    }
    // AG Ok
    function parent(Tree storage self, uint key) internal view returns (uint _parent) {
        // AG Ok
        require(key != SENTINEL);
        // AG Ok
        _parent = self.nodes[key].parent;
    }
    // AG Ok
    function grandparent(Tree storage self, uint key) internal view returns (uint _grandparent) {
        // AG Ok
        require(key != SENTINEL);
        // AG Ok
        uint _parent = self.nodes[key].parent;
        // AG Ok
        if (_parent != SENTINEL) {
            // AG Ok
            _grandparent = self.nodes[_parent].parent;
        // AG Ok
        } else {
            // AG Ok
            _grandparent = SENTINEL;
        }
    }
    // AG Ok
    function sibling(Tree storage self, uint key) internal view returns (uint _sibling) {
        // AG Ok
        require(key != SENTINEL);
        // AG Ok
        uint _parent = self.nodes[key].parent;
        // AG Ok
        if (_parent != SENTINEL) {
            // AG Ok
            if (key == self.nodes[_parent].left) {
                // AG Ok
                _sibling = self.nodes[_parent].right;
            // AG Ok
            } else {
                // AG Ok
                _sibling = self.nodes[_parent].left;
            }
        // AG Ok
        } else {
            // AG Ok
            _sibling = SENTINEL;
        }
    }
    // AG Ok
    function uncle(Tree storage self, uint key) internal view returns (uint _uncle) {
        // AG Ok
        require(key != SENTINEL);
        // AG Ok
        uint _grandParent = grandparent(self, key);
        // AG Ok
        if (_grandParent != SENTINEL) {
            // AG Ok
            uint _parent = self.nodes[key].parent;
            // AG Ok
            _uncle = sibling(self, _parent);
        // AG Ok
        } else {
            // AG Ok
            _uncle = SENTINEL;
        }
    }
    // AG Ok
    function insert(Tree storage self, uint z) internal {
        // AG Ok
        require(z != SENTINEL);
        // AG Ok
        bool duplicateFound = false;
        // AG Ok       
        uint y = SENTINEL;
        // AG Ok
        uint x = self.root;
        // AG Ok
        while (x != SENTINEL) {
            // AG Ok
            y = x;
            // AG Ok
            if (z < x) {
                // AG Ok - Moves down the tree
                x = self.nodes[x].left;
            // AG Ok - Could make individual if z == x statement vs nested
            } else {
                // AG Ok
                if (z == x) {
                    // AG Ok    
                    duplicateFound = true;
                    // AG Ok
                    break;
                }
                // AG Ok - See not above else statement
                x = self.nodes[x].right;
            }
        }
        // AG Ok
        require(!duplicateFound);
        // AG Ok -  New node
        self.nodes[z] = Node(y, SENTINEL, SENTINEL, true);
        // AG Ok - Leaf is null, z is head of tree
        if (y == SENTINEL) {
            // AG Ok
            self.root = z;
        // AG Ok
        } else if (z < y) {
            // AG Ok
            self.nodes[y].left = z;
        // AG Ok
        } else {
            // AG Ok
            self.nodes[y].right = z;
        }
        // AG Ok
        insertFixup(self, z);
        // AG Ok
        self.inserted++;
    }

    // AG Ok
    function remove(Tree storage self, uint z) internal {
        // AG Ok
        require(z != SENTINEL);
        // AG Ok
        uint x;
        // AG Ok
        uint y;

        // z can be root OR z is not root && parent cannot be the SENTINEL
        // AG Ok
        require(z == self.root || (z != self.root && self.nodes[z].parent != SENTINEL));
        // AG Ok
        if (self.nodes[z].left == SENTINEL || self.nodes[z].right == SENTINEL) {
            // AG Ok
            y = z;
        // AG Ok - If not leaf of RB tree, try get the closest value above z
        } else {
            // AG Ok
            y = self.nodes[z].right;
            // AG Ok
            while (self.nodes[y].left != SENTINEL) {
                // AG Ok
                y = self.nodes[y].left;
            }
        }
        // AG Ok - maybe add if(y = z) as that is really what you're trying to do, not a left lookup, or add it in the if statement above
        if (self.nodes[y].left != SENTINEL) {
            // AG Ok
            x = self.nodes[y].left;
        // AG Ok
        } else {
            // AG Ok
            x = self.nodes[y].right;
        }
        // AG Ok - Check if parent can be z?
        uint yParent = self.nodes[y].parent;
        // AG Ok - Check if x is not sentinel before assigning it
        self.nodes[x].parent = yParent;
        // AG Ok
        if (yParent != SENTINEL) {
            // AG Ok
            if (y == self.nodes[yParent].left) {
                // AG Ok
                self.nodes[yParent].left = x;
            // AG Ok
            } else {
                // AG Ok
                self.nodes[yParent].right = x;
            }
        // AG Ok
        } else {
            // AG Ok
            self.root = x;
        }
        // AG Ok
        bool doFixup = !self.nodes[y].red;
        // AG Ok
        if (y != z) {
            // AG Ok - Moving next highest number to replace z
            replaceParent(self, y, z);
            // AG Ok
            self.nodes[y].left = self.nodes[z].left;
            // AG Ok
            self.nodes[self.nodes[y].left].parent = y;
            // AG Ok
            self.nodes[y].right = self.nodes[z].right;
            // AG Ok - Reattach parent to next highest value
            self.nodes[self.nodes[y].right].parent = y;
            // AG Ok
            self.nodes[y].red = self.nodes[z].red;
            // AG Ok - Swapping variables
            (y, z) = (z, y);
        }
        // AG Ok
        if (doFixup) {
            // AG Ok
            removeFixup(self, x);
        }
        // Below `delete self.nodes[SENTINEL]` may not be necessary
        // TODO - Remove after testing
        // emit Log("remove", "before delete self.nodes[0]", 0, self.nodes[0].parent, self.nodes[0].left, self.nodes[0].right, self.nodes[0].red);
        // emit Log("remove", "before delete self.nodes[SENTINEL]", SENTINEL, self.nodes[SENTINEL].parent, self.nodes[SENTINEL].left, self.nodes[SENTINEL].right, self.nodes[SENTINEL].red);
        if (self.nodes[SENTINEL].parent != SENTINEL) {
            delete self.nodes[SENTINEL];
        }
        delete self.nodes[y];
        self.removed++;
    }
    // AG Ok - T: What if you put a key on the right of the tree root?
    function treeMinimum(Tree storage self, uint key) private view returns (uint) {
        // AG Ok
        while (self.nodes[key].left != SENTINEL) {
            // AG Ok
            key = self.nodes[key].left;
        }
        // AG Ok
        return key;
    }
    // AG Ok
    function treeMaximum(Tree storage self, uint key) private view returns (uint) {
        // AG Ok
        while (self.nodes[key].right != SENTINEL) {
            // AG Ok
            key = self.nodes[key].right;
        }
        // AG Ok
        return key;
    }

    function rotateLeft(Tree storage self, uint x) private {
        uint y = self.nodes[x].right;
        uint _parent = self.nodes[x].parent;
        uint yLeft = self.nodes[y].left;
        self.nodes[x].right = yLeft;
        if (yLeft != SENTINEL) {
            self.nodes[yLeft].parent = x;
        }
        self.nodes[y].parent = _parent;
        if (_parent == SENTINEL) {
            self.root = y;
        } else if (x == self.nodes[_parent].left) {
            self.nodes[_parent].left = y;
        } else {
            self.nodes[_parent].right = y;
        }
        self.nodes[y].left = x;
        self.nodes[x].parent = y;
    }
    function rotateRight(Tree storage self, uint x) private {
        uint y = self.nodes[x].left;
        uint _parent = self.nodes[x].parent;
        uint yRight = self.nodes[y].right;
        self.nodes[x].left = yRight;
        if (yRight != SENTINEL) {
            self.nodes[yRight].parent = x;
        }
        self.nodes[y].parent = _parent;
        if (_parent == SENTINEL) {
            self.root = y;
        } else if (x == self.nodes[_parent].right) {
            self.nodes[_parent].right = y;
        } else {
            self.nodes[_parent].left = y;
        }
        self.nodes[y].right = x;
        self.nodes[x].parent = y;
    }

    function insertFixup(Tree storage self, uint z) private {
        uint y;

        while (z != self.root && self.nodes[self.nodes[z].parent].red) {
            uint zParent = self.nodes[z].parent;
            if (zParent == self.nodes[self.nodes[zParent].parent].left) {
                y = self.nodes[self.nodes[zParent].parent].right;
                if (self.nodes[y].red) {
                    self.nodes[zParent].red = false;
                    self.nodes[y].red = false;
                    self.nodes[self.nodes[zParent].parent].red = true;
                    z = self.nodes[zParent].parent;
                } else {
                    if (z == self.nodes[zParent].right) {
                      z = zParent;
                      rotateLeft(self, z);
                    }
                    zParent = self.nodes[z].parent;
                    self.nodes[zParent].red = false;
                    self.nodes[self.nodes[zParent].parent].red = true;
                    rotateRight(self, self.nodes[zParent].parent);
                }
            } else {
                y = self.nodes[self.nodes[zParent].parent].left;
                if (self.nodes[y].red) {
                    self.nodes[zParent].red = false;
                    self.nodes[y].red = false;
                    self.nodes[self.nodes[zParent].parent].red = true;
                    z = self.nodes[zParent].parent;
                } else {
                    if (z == self.nodes[zParent].left) {
                      z = zParent;
                      rotateRight(self, z);
                    }
                    zParent = self.nodes[z].parent;
                    self.nodes[zParent].red = false;
                    self.nodes[self.nodes[zParent].parent].red = true;
                    rotateLeft(self, self.nodes[zParent].parent);
                }
            }
        }
        self.nodes[self.root].red = false;
    }

    function replaceParent(Tree storage self, uint a, uint b) private {
        uint bParent = self.nodes[b].parent;
        self.nodes[a].parent = bParent;
        if (bParent == SENTINEL) {
            self.root = a;
        } else {
            if (b == self.nodes[bParent].left) {
                self.nodes[bParent].left = a;
            } else {
                self.nodes[bParent].right = a;
            }
        }
    }
    function removeFixup(Tree storage self, uint x) private {
        uint w;
        while (x != self.root && !self.nodes[x].red) {
            uint xParent = self.nodes[x].parent;
            if (x == self.nodes[xParent].left) {
                w = self.nodes[xParent].right;
                if (self.nodes[w].red) {
                    self.nodes[w].red = false;
                    self.nodes[xParent].red = true;
                    rotateLeft(self, xParent);
                    w = self.nodes[xParent].right;
                }
                if (!self.nodes[self.nodes[w].left].red && !self.nodes[self.nodes[w].right].red) {
                    self.nodes[w].red = true;
                    x = xParent;
                } else {
                    if (!self.nodes[self.nodes[w].right].red) {
                        self.nodes[self.nodes[w].left].red = false;
                        self.nodes[w].red = true;
                        rotateRight(self, w);
                        w = self.nodes[xParent].right;
                    }
                    self.nodes[w].red = self.nodes[xParent].red;
                    self.nodes[xParent].red = false;
                    self.nodes[self.nodes[w].right].red = false;
                    rotateLeft(self, xParent);
                    x = self.root;
                }
            } else {
                w = self.nodes[xParent].left;
                if (self.nodes[w].red) {
                    self.nodes[w].red = false;
                    self.nodes[xParent].red = true;
                    rotateRight(self, xParent);
                    w = self.nodes[xParent].left;
                }
                if (!self.nodes[self.nodes[w].right].red && !self.nodes[self.nodes[w].left].red) {
                    self.nodes[w].red = true;
                    x = xParent;
                } else {
                    if (!self.nodes[self.nodes[w].left].red) {
                        self.nodes[self.nodes[w].right].red = false;
                        self.nodes[w].red = true;
                        rotateLeft(self, w);
                        w = self.nodes[xParent].left;
                    }
                    self.nodes[w].red = self.nodes[xParent].red;
                    self.nodes[xParent].red = false;
                    self.nodes[self.nodes[w].left].red = false;
                    rotateRight(self, xParent);
                    x = self.root;
                }
            }
        }
        self.nodes[x].red = false;
    }
}
// ----------------------------------------------------------------------------
// End - BokkyPooBah's Red-Black Tree Library
// ----------------------------------------------------------------------------

```
