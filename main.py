import math

# attributes = {Type: ["French",, Italian, "Thai",], Patrons: [], Hungry: [], ... Fri/Sat: []}
# attribute_values = Type: ["French",, Italian, "Thai",]   //ex. Type
# examples = [{id: <id>, Patrons: <Patrons>, Hungry: <Hungry>, Type: <Type> ... }, {.....}, {.....}]

class Node:
    def __init__(self, goal_value=""):     
        self.children = []
        self.attribute = ""
        self.attr_value = ""
        self.goal_value = goal_value  # if leaf node


def entropy(q):     # entropy of a boolean random variable q = pos / (pos+neg)
    if q == 0:
        return -1 * (1-q) * math.log(1-q, 2)
    if q == 1:
        return -1 * q * math.log(q, 2)
    return -1 * (q * math.log(q, 2) + (1-q) * math.log(1-q, 2))


def get_attribute_probabilities(attribute, attributes, examples):
    # {"French",: [4, 6], } pos, neg
    attr_dict = {}
    for attr_val in attributes[attribute]:
        attr_dict[attr_val] = [0, 0]
    for example in examples:
        if example[goal] == positive:
            attr_dict[example.get(attribute)][0] += 1
        else:
            attr_dict[example.get(attribute)][1] += 1
    return attr_dict


def get_examples_pos_probability(examples):
    pos_prob = 0
    for example in examples:
        if example[goal] == positive:
            pos_prob += 1 
    return pos_prob/len(examples)


def remainder(attribute, attributes, examples):
    attr_sum = 0
    attr_dict = get_attribute_probabilities(attribute, attributes, examples)
    for attribute in attr_dict.keys():
        positives = attr_dict[attribute][0]
        negatives = attr_dict[attribute][1]
        if positives + negatives == 0:
            continue
        attr_sum += (positives + negatives) * entropy(positives / (positives + negatives))
    return 1/len(examples) * attr_sum


def importance(attribute, attributes, examples):
    return entropy(get_examples_pos_probability(examples)) - remainder(attribute, attributes, examples)


def plurality_value(examples):
    positive_count = 0
    negative_count = 0
    for example in examples:
        if example[goal] == positive:
            positive_count += 1
        else:
            negative_count += 1
    return positive if positive_count >= negative_count else negative


def eliminate_attributes(node):
    if len(node.children) == 0:
        return
    child0 = node.children[0]
    for child in node.children:
        if child0.goal_value != child.goal_value:
            return
    if child0.goal_value == "":
        return
    node.goal_value = child0.goal_value
    node.children = []


def pruning(root):
    for i in range(depth+1):
        queue = [root]
        while queue:
            level_size = len(queue)
            while level_size > 0:
                node = queue.pop(0)
                eliminate_attributes(node)
                level_size -= 1
                for child in node.children:
                    queue += [child]


def check_if_all_same(examples):
    first_example = examples[0][goal]
    for example in examples:
        if example[goal] != first_example:
            return False, None
    return True, first_example


def arg_max_importance(attributes, examples):
    curr_max = float('-inf')
    max_arg = ""
    for a in attributes:
        if a == goal or a == id_ignored:
            continue
        gain = importance(a, attributes, examples)
        if gain > curr_max:
            curr_max = gain
            max_arg = a
    return max_arg


def create_new_examples(attribute, attribute_value, parent_examples):
    new_examples = []
    for example in parent_examples:
        if example[attribute] == attribute_value:
            new_examples.append(example)
    return new_examples


def create_new_attributes(attribute, attributes):
    new_attributes = {}
    for attr in attributes.keys():
        if attr == attribute:
            continue
        new_attributes[attr] = attributes[attr]
    return new_attributes


def decision_tree_learning(attributes, examples, parent_examples):
    global depth
    depth = 1
    if len(examples) == 0:
        tree = Node(plurality_value(parent_examples))
        return tree

    all_same_class = check_if_all_same(examples)
    if all_same_class[0]:
        tree = Node(all_same_class[1])
        return tree
    
    if len(attributes) == 2:    # id and goal attributes are ignored
        return Node(plurality_value(examples))

    attribute = arg_max_importance(attributes, examples)
    tree = Node()
    for val in attributes[attribute]:
        new_examples = create_new_examples(attribute, val, examples)
        new_attributes = create_new_attributes(attribute, attributes)
        subtree = decision_tree_learning(new_attributes, new_examples, examples)
        subtree.attribute = attribute
        subtree.attr_value = val
        tree.children.append(subtree)
    depth += 1
    return tree


# {"Attribute1": [attr_val1, attr_val2, ...], ...}
def get_attributes_from_examples(examples, first_line):
    attributes = {}
    for column in first_line:
        attributes[column] = []
    for example in examples:
        for key in example.keys():
            if example[key] in attributes[key]:
                continue
            attributes[key].append(example[key])
    return attributes


def bfs_print(root):
    queue = [root]
    while queue:
        level_size = len(queue)
        while level_size > 0:
            node = queue.pop(0)
            level_size -= 1
            print(f"{node.attribute}:{node.attr_value}({node.goal_value})", end=" ")
            for child in node.children:
                queue += [child]
        print()


def get_data_from_csv(g, pos, neg, file_name):
    global goal     # EatOur or TitanicSurvived ...
    global positive # True or 0 ...
    global negative 
    goal = g
    positive = pos
    negative = neg
    data_file = open(file_name, "r")
    columns = data_file.readline().strip().split(",")
    examples = []
    for line in data_file.readlines():
        data = line.strip().split(",")
        data_dict = dict()
        for i in range(len(columns)):
            data_dict[columns[i]] = data[i]
        examples.append(data_dict)
    return examples, columns


def calculate_error(data, root):
    incorrect_count = 0
    for example in data:
        if example[goal] != find_val(example, root):
            incorrect_count += 1
    return incorrect_count / len(data)


def k_fold(k, examples, test_data):
    partial_len = int(len(examples)/k)

    e_gen = 0
    test_errors = []
    for i in range(k):
        train_data = examples[ : (i * partial_len)] + examples[(i+1) * partial_len: ]
        validate_data = examples[i * partial_len: (i+1) * partial_len]
        root = train(train_data)
        pruning(root)
#        bfs_print(root)
        print(i, calculate_error(validate_data, root))
        e_gen += (calculate_error(validate_data, root))
        test_errors.append(calculate_error(test_data, root))
    return e_gen/k, test_errors


def find_val(example, node):
    if node.goal_value != "":
        return node.goal_value
    for child in node.children:
        if example.get(child.attribute) == child.attr_value:
            return find_val(example, child)   


def test(test_data, root):
    return calculate_error(test_data, root)


def train(train_data):
    attributes = get_attributes_from_examples(train_data, columns)
    return decision_tree_learning(attributes, train_data, train_data)


if __name__ == "__main__":
    global columns
    global id_ignored
    examples, columns = get_data_from_csv("Loan_Status", "Y", "N", "training.csv")
    id_ignored = columns[0]

    test_data = get_data_from_csv("Loan_Status", "Y", "N", "test.csv")[0]
    print(k_fold(5, examples, test_data))
