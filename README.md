# MSML606 Homework Assignment 2
```
Name: Amey Hengle
UID: 122283961
Email: ameyhen@umd.edu
```

## project structure

| component | description |
|---|---|
| `TreeNode` | represents a single node (operator or operand) in the tree |
| `TraversalOrder` | enum driving prefix, infix, and postfix traversal logic |
| `HomeWork2` | builds the tree and handles all three traversal prints |
| `Stack` | evaluates a postfix expression string directly |

---

## sample runs

### problem 1 — expression tree construction

The input is a postfix token list. the tree is built using a stack: operands become leaf nodes, operators pop two nodes and become their parent.

```python
hw2 = HomeWork2()

postfix_input = ["3", "4", "+", "2", "*"]
print(f"Input Postfix Array: {postfix_input}")

root_node = hw2.constructBinaryTree(postfix_input)
printTree(root_node)
```

**output:**
```
========================================
PROBLEM 1: Expression Tree Construction
========================================
Input Postfix Array: ['3', '4', '+', '2', '*']

Visual Tree Representation (Read Left to Right):
    ┌── 2
└── *
        ┌── 4
    └── +
        └── 3
```


---

### problem 2 — tree traversals

using the tree built in problem 1, all three standard traversal orders are printed.

```python
print(f"Prefix:  {hw2.prefixNotationPrint(root_node)}")
print(f"Infix:   {hw2.infixNotationPrint(root_node)}")
print(f"Postfix: {hw2.postfixNotationPrint(root_node)}")
```

**output:**
```
========================================
PROBLEM 2: Tree Traversals
========================================
Prefix:  ['*', '+', '3', '4', '2']
Infix:   ['(', '(', '3', '+', '4', ')', '*', '2', ')']
Postfix: ['3', '4', '+', '2', '*']
```

| order | description |
|---|---|
| prefix | root first, then children — useful for copying trees |
| infix | fully parenthesised left-to-right — human-readable form |
| postfix | children before root — reconstructs the original input |

---

### problem 3 — postfix evaluation via stack

a raw postfix string is passed in, scanned token by token, and evaluated using stack arithmetic.

```python
my_stack = Stack()
postfix_str = "5 1 2 + 4 * + 3 -"
result = my_stack.evaluatePostfix(postfix_str)
print(f"Evaluation Result: {result}")
```

**output:**
```
========================================
PROBLEM 3: Postfix Evaluation via Stack
========================================
String Expression: '5 1 2 + 4 * + 3 -'
Evaluation Result: 14
```

the expression `5 1 2 + 4 * + 3 -` resolves as `5 + ((1 + 2) * 4) - 3 = 14`.

---

### problem 4 — edge cases

Following edge cases were considered across the implementation. some are fully handled, and others are noted as known limitations.

---

#### empty postfix expressions

**what happens:** `constructBinaryTree` checks `if not input_list` as its very first step and returns `None` immediately. all traversal methods also open with `if node is None: return []`, so printing an empty tree is equally safe — nothing crashes.

```python
hw2.constructBinaryTree([])   # returns None safely
hw2.prefixNotationPrint(None) # returns [] safely
```

---

#### malformed postfix expressions

**what happens:** two explicit `ValueError` raises cover both failure modes.

- **too few operands** — if an operator is hit but the stack has fewer than two nodes, it raises immediately with a message naming the offending operator.
- **too many operands** — if the loop finishes and more than one node remains on the stack, the expression had unresolved operands and raises accordingly.

```python
# too few operands
hw2.constructBinaryTree(["+", "3"])
# raises: ValueError: malformed expression: insufficient operands for operator '+'

# too many operands
hw2.constructBinaryTree(["3", "4", "5", "+"])
# raises: ValueError: malformed expression: 2 operand(s) left unresolved.
```

---

#### division by zero

**current status: not handled.**

`constructBinaryTree` only builds the tree — it never performs arithmetic. division by zero would only surface in a separate evaluation step. if one were added, an explicit guard before any division operation would be needed.

```python
# tree builds fine — no evaluation happens here
hw2.constructBinaryTree(["5", "0", "/"])

# a future evaluator would need something like:
if operator == '/' and right_operand == 0:
    raise ZeroDivisionError("division by zero in expression.")
```

---

#### invalid tokens

**current status: not handled.**

Anything that isn't in `_OPERATORS` is treated as a valid operand and silently wrapped into a leaf node. a token like `"abc"` or `"@"` would enter the tree without complaint. guarding against this would require a validation step that checks whether non-operator tokens are actually numeric before pushing them onto the stack.

```python
# no error raised — "abc" just becomes a leaf node
hw2.constructBinaryTree(["abc", "3", "+"])
```

---

#### very large numbers or results

**current status: not a concern at the tree level.**

The tree only stores tokens — no arithmetic is performed during construction or traversal. python also handles arbitrarily large integers natively, so integer overflow is a non-issue. floating point precision could still degrade for very large `float` values, but that is a python-level limitation rather than something this implementation needs to address.

---

#### negative numbers in the expression

**current status: works if pre-tokenized, fragile if not.**

if negative numbers arrive as already-parsed tokens in the list (e.g. `"-3"` as a single string), they are wrapped into leaf nodes without issue. the problem arises if a raw string is naively split on spaces, because `"-3"` could be misread as the operator `"-"` followed by `"3"`. since `constructBinaryTree` accepts a pre-split list, correct tokenization is the caller's responsibility.

```python
# works fine — "-3" is treated as a single operand token
hw2.constructBinaryTree(["-3", "4", "+"])
```
