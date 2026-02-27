import csv
from __future__ import annotations
from enum import Enum
from typing import Optional

dashed_line = '-'*50

class TreeNode:
    """
    represents a single node in a binary expression tree.
    holds a value (operator or operand) and optional left/right children.
    """
    __slots__ = ("val", "left", "right")

    def __init__(self, val=0, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None):
        self.val   = val
        self.left  = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val!r})"

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    

class TraversalOrder(Enum):
    PREFIX  = "prefix"
    INFIX   = "infix"
    POSTFIX = "postfix"
    

class HomeWork2:

    _OPERATORS: frozenset[str] = frozenset({'+', '-', '*', '/'})

    # ------------------------------------------------------------------
    # tree construction
    # ------------------------------------------------------------------

    def constructBinaryTree(self, input_list: list) -> Optional[TreeNode]:
        """
        builds a binary expression tree from a postfix (RPN) token list.

        algorithm:
          - scan tokens left-to-right.
          - operand  → wrap in a leaf node and push onto the stack.
          - operator → pop two nodes (right then left), create a parent
                       node, and push it back.
          - one node remaining at the end becomes the tree root.
        """
        if not input_list:
            return None

        stack: list[TreeNode] = []

        for token in input_list:
            if token not in self._OPERATORS:
                # operand — just wrap it in a leaf and stack it
                stack.append(TreeNode(token))
            else:
                # need at least two operands to apply an operator
                if len(stack) < 2:
                    raise ValueError(
                        f"malformed expression: insufficient operands for operator '{token}'."
                    )
                # pop right before left — order matters here
                right_node, left_node = stack.pop(), stack.pop()
                stack.append(TreeNode(token, left_node, right_node))

        # anything other than exactly one root means the expression was off
        if len(stack) != 1:
            raise ValueError(
                f"malformed expression: {len(stack)} operand(s) left unresolved."
            )

        return stack.pop()

    # ------------------------------------------------------------------
    # traversal — public api
    # ------------------------------------------------------------------

    def prefixNotationPrint(self, head: Optional[TreeNode]) -> list:
        """returns tokens in prefix (root → left → right) order."""
        return self._traverse(head, TraversalOrder.PREFIX)

    def infixNotationPrint(self, head: Optional[TreeNode]) -> list:
        """returns tokens in fully-parenthesised infix order."""
        return self._traverse(head, TraversalOrder.INFIX)

    def postfixNotationPrint(self, head: Optional[TreeNode]) -> list:
        """returns tokens in postfix (left → right → root) order."""
        return self._traverse(head, TraversalOrder.POSTFIX)

    # ------------------------------------------------------------------
    # traversal — unified private engine
    # ------------------------------------------------------------------

    def _traverse(self, node: Optional[TreeNode], order: TraversalOrder) -> list:
        """
        single recursive engine that drives all three traversals.
        the TraversalOrder enum selects where the current node's value
        is inserted relative to its children's results.
        """
        if node is None:
            return []

        # leaf nodes carry no operator — skip parentheses for infix
        if order is TraversalOrder.INFIX and node.is_leaf:
            return [node.val]

        left_tokens  = self._traverse(node.left,  order)
        right_tokens = self._traverse(node.right, order)

        # each order just differs in where the current value gets slotted in
        assembly = {
            TraversalOrder.PREFIX:  [node.val] + left_tokens + right_tokens,
            TraversalOrder.INFIX:   ['('] + left_tokens + [node.val] + right_tokens + [')'],
            TraversalOrder.POSTFIX: left_tokens + right_tokens + [node.val],
        }

        return assembly[order]

def printTree(node, prefix="", is_left=True, is_root=True):
    if node is not None:
        printTree(node.right, prefix + ("    " if is_left or is_root else "│   "), False, False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.val))
        printTree(node.left, prefix + ("│   " if is_left and not is_root else "    "), True, False)


class Stack:
    def __init__(self):
        self.items = []
        self.top_index = -1  # starts at -1 to indicate an empty stack

    def push(self, item):
        self.items.append(item)
        self.top_index += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        item = self.items[self.top_index]
        del self.items[self.top_index]
        self.top_index -= 1
        return item

    def is_empty(self):
        return self.top_index == -1

    def evaluatePostfix(self, exp: str) -> int:
        # edge case: empty postfix expressions
        if not exp or not exp.strip():
            raise ValueError("Empty expression provided.")

        tokens = exp.split()
        operators = {'+', '-', '*', '/'}

        for token in tokens:
            if token not in operators:
                # edge case: invalid non-numeric tokens — can't push garbage onto the stack
                try:
                    self.push(int(token))
                except ValueError:
                    raise ValueError(f"Invalid token encountered: {token}")
            else:
                # edge case: not enough operands sitting on the stack for this operator
                if self.top_index < 1:
                    raise ValueError("Invalid postfix expression: insufficient operands.")
                
                right_val = self.pop()
                left_val = self.pop()
                
                if token == '+':
                    self.push(left_val + right_val)
                elif token == '-':
                    self.push(left_val - right_val)
                elif token == '*':
                    self.push(left_val * right_val)
                elif token == '/':
                    # edge case: can't divide by zero, bail out early
                    if right_val == 0:
                        raise ZeroDivisionError("DIVZERO")
                    
                    self.push(int(left_val / right_val))
        
        # edge case: too many operands left over — expression was malformed
        if self.top_index != 0:
            raise ValueError("Invalid postfix expression: too many operands left.")
            
        return self.pop()

    
if __name__ == "__main__":
        
    homework2 = HomeWork2()

    print("\nRUNNING TEST CASES FOR PROBLEM 1")
    testcases = []
    try:
        with open('p1_construct_tree.csv', 'r') as f:
            testcases = list(csv.reader(f))
    except FileNotFoundError:
        print("p1_construct_tree.csv not found")

    for i, (postfix_input,) in enumerate(testcases, 1):
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
        output = homework2.postfixNotationPrint(root)

        assert output == postfix, f"P1 Test {i} failed: tree structure incorrect"
        print(f"P1 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 2")
    testcases = []
    with open('p2_traversals.csv', 'r') as f:
        testcases = list(csv.reader(f))

    for i, row in enumerate(testcases, 1):
        postfix_input, exp_pre, exp_in, exp_post = row
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)

        assert homework2.prefixNotationPrint(root) == exp_pre.split(","), f"P2-{i} prefix failed"
        assert homework2.infixNotationPrint(root) == exp_in.split(","), f"P2-{i} infix failed"
        assert homework2.postfixNotationPrint(root) == exp_post.split(","), f"P2-{i} postfix failed"

        print(f"P2 Test {i} passed")
        print(dashed_line)

    print("\nRUNNING TEST CASES FOR PROBLEM 3")
    testcases = []
    try:
        with open('p3_eval_postfix.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                testcases.append(row)
    except FileNotFoundError:
        print("p3_eval_postfix.csv not found")

    for idx, row in enumerate(testcases, start=1):
        expr, expected = row

        try:
            s = Stack()
            result = s.evaluatePostfix(expr)
            if expected == "DIVZERO":
                print(f"Test {idx} failed (expected division by zero)")
            else:
                expected = int(expected)
                assert result == expected, f"Test {idx} failed: {result} != {expected}"
                print(f"Test case {idx} passed")

        except ZeroDivisionError:
            assert expected == "DIVZERO", f"Test {idx} unexpected division by zero"
            print(f"Test case {idx} passed (division by zero handled)")