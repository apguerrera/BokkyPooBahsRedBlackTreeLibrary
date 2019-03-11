# BokkyPooBah's Red-Black Tree Library

Source file [../../contracts/BokkyPooBahsRedBlackTreeLibrary.sol](../../contracts/BokkyPooBahsRedBlackTreeLibrary.sol).

<br />

<hr />

```javascript
// AG Ok
pragma solidity ^0.5.4;

// ----------------------------------------------------------------------------
// BokkyPooBah's Red-Black Tree Library v1.0-pre-release-a
//
// A Solidity Red-Black Tree binary search library to store and access a sorted
// list of unsigned integer data. The Red-Black algorithm rebalances the binary
// search tree, resulting in O(log n) insert, remove and search time (and ~gas)
//
// https://github.com/bokkypoobah/BokkyPooBahsRedBlackTreeLibrary
//
//
// Enjoy. (c) BokkyPooBah / Bok Consulting Pty Ltd 2019. The MIT Licence.
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
    }
    // AG Ok - EMPTY can be set to non null if 0 is a required key  
    uint private constant EMPTY = 0;
    // AG Ok
    function first(Tree storage self) internal view returns (uint _key) {
        // AG Ok
        _key = self.root;
        // AG Ok
        if (_key != EMPTY) {
            // AG Ok - Might want to use treeMinimum(_key) for consistency  
            while (self.nodes[_key].left != EMPTY) {
                // AG Ok
                _key = self.nodes[_key].left;
            }
        }
    }
    // AG Ok
    function last(Tree storage self) internal view returns (uint _key) {
        // AG Ok
        _key = self.root;
        // AG Ok
        if (_key != EMPTY) {
            // AG Ok - Might want to use treeMaximum(_key) for consistency  
            while (self.nodes[_key].right != EMPTY) {
                // AG Ok
                _key = self.nodes[_key].right;
            }
        }
    }
    // AG Ok
    function next(Tree storage self, uint target) internal view returns (uint cursor) {
        // AG Ok
        require(target != EMPTY);
        // AG Ok
        if (self.nodes[target].right != EMPTY) {
            // AG Ok
            cursor = treeMinimum(self, self.nodes[target].right);
        } else {
            // AG OK - Up the tree
            cursor = self.nodes[target].parent;
            // AG OK - Progress up the tree until it discovers the next highest node
            while (cursor != EMPTY && target == self.nodes[cursor].right) {
                // AG Ok
                target = cursor;
                // AG Ok
                cursor = self.nodes[cursor].parent;
            }
        }
    }
    // AG Ok - Symmetrical to next()
    function prev(Tree storage self, uint target) internal view returns (uint cursor) {
        // AG Ok
        require(target != EMPTY);
        // AG Ok
        if (self.nodes[target].left != EMPTY) {
            // AG Ok
            cursor = treeMaximum(self, self.nodes[target].left);
        // AG Ok
        } else {
            // AG Ok
            cursor = self.nodes[target].parent;
            // AG Ok
            while (cursor != EMPTY && target == self.nodes[cursor].left) {
                // AG Ok
                target = cursor;
                // AG Ok
                cursor = self.nodes[cursor].parent;
            }
        }
    }
    // AG Ok - Nice improvement from the 0.9 version!
    function exists(Tree storage self, uint key) internal view returns (bool) {
        // AG Ok - Could be explicit and add a two way check for parent node
        return (key != EMPTY) && ((key == self.root) || (self.nodes[key].parent != EMPTY));
    }
    // AG Ok
    function isEmpty(uint key) internal pure returns (bool) {
        // AG Ok
        return key == EMPTY;
    }
    // AG Ok
    function getEmpty() internal pure returns (uint) {
        // AG Ok
        return EMPTY;
    }
    // AG Ok - Again, nice improvement from the 0.9 version!
    function getNode(Tree storage self, uint key) internal view returns (uint _returnKey, uint _parent, uint _left, uint _right, bool _red) {
        // AG Ok
        require(exists(self, key));
        // AG Ok - Holds true for empty node
        return(key, self.nodes[key].parent, self.nodes[key].left, self.nodes[key].right, self.nodes[key].red);
    }
    // AG Ok
    function insert(Tree storage self, uint key) internal {
        // AG Ok
        require(key != EMPTY);
        // AG Ok
        require(!exists(self, key));
        // AG Ok
        uint cursor = EMPTY;
        // AG Ok
        uint probe = self.root;
        // AG Ok
        while (probe != EMPTY) {
            // AG Ok
            cursor = probe;
            // AG Ok - Moves down the tree
            if (key < probe) {
                // AG Ok
                probe = self.nodes[probe].left;
            // AG Ok
            } else {
                // AG Ok  
                probe = self.nodes[probe].right;
            }
        }
        // AG Ok -  New node
        self.nodes[key] = Node({parent: cursor, left: EMPTY, right: EMPTY, red: true});
        // AG Ok
        if (cursor == EMPTY) {
            // AG Ok
            self.root = key;
        // AG Ok
        } else if (key < cursor) {
            // AG Ok
            self.nodes[cursor].left = key;
        // AG Ok
        } else {
            // AG Ok
            self.nodes[cursor].right = key;
        }
        // AG Ok
        insertFixup(self, key);
    }

    // AG Ok
    function remove(Tree storage self, uint key) internal {
        // AG Ok
        require(key != EMPTY);
        // AG Ok - replaces old v0.9 require()
        require(exists(self, key));
        // AG Ok
        uint probe;
        // AG Ok
        uint cursor;
        // AG Ok
        if (self.nodes[key].left == EMPTY || self.nodes[key].right == EMPTY) {
            // AG Ok
            cursor = key;
        // AG Ok - If not leaf of RB tree, try get the closest value above key
        } else {
            // AG Ok
            cursor = self.nodes[key].right;
            // AG Ok
            while (self.nodes[cursor].left != EMPTY) {
                // AG Ok
                cursor = self.nodes[cursor].left;
            }
        }
        // AG Ok - maybe add if(cursor = key) as that is really what you're trying to do, not a left lookup, or add it in the if statement above
        if (self.nodes[cursor].left != EMPTY) {
            // AG Ok
            probe = self.nodes[cursor].left;
        // AG Ok
        } else {
            // AG Ok
            probe = self.nodes[cursor].right;
        }
        // AG Ok - Check if parent can be key?
        uint yParent = self.nodes[cursor].parent;
        // AG Ok - Check if cursor is not sentinel before assigning it
        self.nodes[probe].parent = yParent;
        // AG Ok
        if (yParent != EMPTY) {
            // AG Ok
            if (cursor == self.nodes[yParent].left) {
                // AG Ok
                self.nodes[yParent].left = probe;
            // AG Ok
            } else {
                // AG Ok
                self.nodes[yParent].right = probe;
            }
        // AG Ok
        } else {
            // AG Ok
            self.root = probe;
        }
        // AG Ok
        bool doFixup = !self.nodes[cursor].red;
        // AG Ok
        if (cursor != key) {
            // AG Ok - Moving next highest number to replace key
            replaceParent(self, cursor, key);
            // AG Ok
            self.nodes[cursor].left = self.nodes[key].left;
            // AG Ok
            self.nodes[self.nodes[cursor].left].parent = cursor;
            // AG Ok
            self.nodes[cursor].right = self.nodes[key].right;
            // AG Ok - Reattach parent to next highest value
            self.nodes[self.nodes[cursor].right].parent = cursor;
            // AG Ok
            self.nodes[cursor].red = self.nodes[key].red;
            // AG Ok - Swapping variables
            (cursor, key) = (key, cursor);
        }
        // AG Ok
        if (doFixup) {
            // AG Ok
            removeFixup(self, probe);
        }
        // AG Ok
        delete self.nodes[cursor];
    }
    // AG Ok - Local Min, if you put a key on the right of the tree root, will return local minima. Might want to clearly document this compared to first()
    function treeMinimum(Tree storage self, uint key) private view returns (uint) {
        // AG Ok
        while (self.nodes[key].left != EMPTY) {
            // AG Ok
            key = self.nodes[key].left;
        }
        // AG Ok
        return key;
    }
    // AG Ok
    function treeMaximum(Tree storage self, uint key) private view returns (uint) {
        // AG Ok
        while (self.nodes[key].right != EMPTY) {
            // AG Ok
            key = self.nodes[key].right;
        }
        // AG Ok
        return key;
    }
    // AG Ok
    function rotateLeft(Tree storage self, uint key) private {
        // AG Ok
        uint cursor = self.nodes[key].right;
        // AG Ok
        uint keyParent = self.nodes[key].parent;
        // AG Ok
        uint cursorLeft = self.nodes[cursor].left;
        // AG Ok - Replace cursor with cursorLeft
        self.nodes[key].right = cursorLeft;
        // AG Ok
        if (cursorLeft != EMPTY) {
            // AG Ok
            self.nodes[cursorLeft].parent = key;
        }
        // AG Ok
        self.nodes[cursor].parent = keyParent;
        // AG Ok
        if (keyParent == EMPTY) {
            // AG Ok
            self.root = cursor;
        // AG Ok - Dependant on keyParent being larger or smaller than key
        } else if (key == self.nodes[keyParent].left) {
            // AG Ok
            self.nodes[keyParent].left = cursor;
        // AG Ok
        } else {
            // AG Ok
            self.nodes[keyParent].right = cursor;
        }
        // AG Ok - reconnecting the two trees bidirectionally
        self.nodes[cursor].left = key;
        // AG Ok
        self.nodes[key].parent = cursor;
    }
    // AG Ok
    function rotateRight(Tree storage self, uint key) private {
        // AG Ok
        uint cursor = self.nodes[key].left;
        // AG Ok
        uint keyParent = self.nodes[key].parent;
        // AG Ok
        uint cursorRight = self.nodes[cursor].right;
        // AG Ok
        self.nodes[key].left = cursorRight;
        // AG Ok
        if (cursorRight != EMPTY) {
            // AG Ok
            self.nodes[cursorRight].parent = key;
        }
        // AG Ok
        self.nodes[cursor].parent = keyParent;
        // AG Ok
        if (keyParent == EMPTY) {
            // AG Ok
            self.root = cursor;
        // AG Ok - Dependant on keyParent being larger or smaller than key
        } else if (key == self.nodes[keyParent].right) {
            // AG Ok
            self.nodes[keyParent].right = cursor;
        // AG Ok
        } else {
            // AG Ok
            self.nodes[keyParent].left = cursor;
        }
        // AG Ok - reconnecting the two trees bidirectionally
        self.nodes[cursor].right = key;
        // AG Ok
        self.nodes[key].parent = cursor;
    }
    
    // AG To Do
    function insertFixup(Tree storage self, uint key) private {
        uint cursor;
        while (key != self.root && self.nodes[self.nodes[key].parent].red) {
            uint keyParent = self.nodes[key].parent;
            if (keyParent == self.nodes[self.nodes[keyParent].parent].left) {
                cursor = self.nodes[self.nodes[keyParent].parent].right;
                if (self.nodes[cursor].red) {
                    self.nodes[keyParent].red = false;
                    self.nodes[cursor].red = false;
                    self.nodes[self.nodes[keyParent].parent].red = true;
                    key = self.nodes[keyParent].parent;
                } else {
                    if (key == self.nodes[keyParent].right) {
                      key = keyParent;
                      rotateLeft(self, key);
                    }
                    keyParent = self.nodes[key].parent;
                    self.nodes[keyParent].red = false;
                    self.nodes[self.nodes[keyParent].parent].red = true;
                    rotateRight(self, self.nodes[keyParent].parent);
                }
            } else {
                cursor = self.nodes[self.nodes[keyParent].parent].left;
                if (self.nodes[cursor].red) {
                    self.nodes[keyParent].red = false;
                    self.nodes[cursor].red = false;
                    self.nodes[self.nodes[keyParent].parent].red = true;
                    key = self.nodes[keyParent].parent;
                } else {
                    if (key == self.nodes[keyParent].left) {
                      key = keyParent;
                      rotateRight(self, key);
                    }
                    keyParent = self.nodes[key].parent;
                    self.nodes[keyParent].red = false;
                    self.nodes[self.nodes[keyParent].parent].red = true;
                    rotateLeft(self, self.nodes[keyParent].parent);
                }
            }
        }
        self.nodes[self.root].red = false;
    }
    // AG Ok -  Used in remove function, from a to b only, not bidirectional
    function replaceParent(Tree storage self, uint a, uint b) private {
        // Ag Ok
        uint bParent = self.nodes[b].parent;
        // AG Ok
        self.nodes[a].parent = bParent;
        // AG Ok
        if (bParent == EMPTY) {
            // AG Ok
            self.root = a;
        // AG Ok - else if bParent is larger or smaller than b
        // AG Note - This is a private function and does as required take care in selecting a and b values
        } else {
            // AG Ok
            if (b == self.nodes[bParent].left) {
                // AG Ok
                self.nodes[bParent].left = a;
            // AG Ok
            } else {
                // AG Ok
                self.nodes[bParent].right = a;
            }
        }
    }

    // AG To Do
    function removeFixup(Tree storage self, uint key) private {
        uint cursor;
        while (key != self.root && !self.nodes[key].red) {
            uint keyParent = self.nodes[key].parent;
            if (key == self.nodes[keyParent].left) {
                cursor = self.nodes[keyParent].right;
                if (self.nodes[cursor].red) {
                    self.nodes[cursor].red = false;
                    self.nodes[keyParent].red = true;
                    rotateLeft(self, keyParent);
                    cursor = self.nodes[keyParent].right;
                }
                if (!self.nodes[self.nodes[cursor].left].red && !self.nodes[self.nodes[cursor].right].red) {
                    self.nodes[cursor].red = true;
                    key = keyParent;
                } else {
                    if (!self.nodes[self.nodes[cursor].right].red) {
                        self.nodes[self.nodes[cursor].left].red = false;
                        self.nodes[cursor].red = true;
                        rotateRight(self, cursor);
                        cursor = self.nodes[keyParent].right;
                    }
                    self.nodes[cursor].red = self.nodes[keyParent].red;
                    self.nodes[keyParent].red = false;
                    self.nodes[self.nodes[cursor].right].red = false;
                    rotateLeft(self, keyParent);
                    key = self.root;
                }
            } else {
                cursor = self.nodes[keyParent].left;
                if (self.nodes[cursor].red) {
                    self.nodes[cursor].red = false;
                    self.nodes[keyParent].red = true;
                    rotateRight(self, keyParent);
                    cursor = self.nodes[keyParent].left;
                }
                if (!self.nodes[self.nodes[cursor].right].red && !self.nodes[self.nodes[cursor].left].red) {
                    self.nodes[cursor].red = true;
                    key = keyParent;
                } else {
                    if (!self.nodes[self.nodes[cursor].left].red) {
                        self.nodes[self.nodes[cursor].right].red = false;
                        self.nodes[cursor].red = true;
                        rotateLeft(self, cursor);
                        cursor = self.nodes[keyParent].left;
                    }
                    self.nodes[cursor].red = self.nodes[keyParent].red;
                    self.nodes[keyParent].red = false;
                    self.nodes[self.nodes[cursor].left].red = false;
                    rotateRight(self, keyParent);
                    key = self.root;
                }
            }
        }
        self.nodes[key].red = false;
    }
}
// ----------------------------------------------------------------------------
// End - BokkyPooBah's Red-Black Tree Library
// ----------------------------------------------------------------------------

```
