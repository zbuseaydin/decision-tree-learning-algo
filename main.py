import math

# attributes = {Type: ["French",, Italian, "Thai",], Patrons: [], Hungry: [], ... Fri/Sat: []}
# attribute_values = Type: ["French",, Italian, "Thai",]   //ex. Type
# examples = [{id: <id>, Patrons: <Patrons>, Hungry: <Hungry>, Type: <Type> ... }, {.....}, {.....}]

class Node:
    def __init__(self):
        self.label = ""
        self.children = []


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
    return positive if positive_count > negative_count else negative


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
    if len(examples) == 0:
        return plurality_value(parent_examples)

    all_same_class = check_if_all_same(examples)
    if all_same_class[0]:
        return all_same_class[1]
    
    if len(attributes) == 0:
        return plurality_value(examples)

    attribute = arg_max_importance(attributes, examples)
    tree = Node()
    for val in attributes[attribute]:
        new_examples = create_new_examples(attribute, val, examples)
        new_attributes = create_new_attributes(attribute, attributes)
        subtree = decision_tree_learning(new_attributes, new_examples, examples)
        if isinstance(subtree, Node):
            subtree.label = f"{attribute}: {val}"
        tree.children.append(subtree)
    return tree


# {"Attribute1": [attr_val1, attr_val2, ...], ...}
def get_attributes_from_examples(examples, first_line):
    attributes = {}
    for column in first_line:
        attributes[column] = []
    for example in examples:
        for key in example.keys():
            if key == goal:
                continue
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
            if isinstance(node, str):
                print(node, end=" ")
                continue
            print(node.label, end=" ")
            for child in node.children:
                queue += [child]
        print()


if __name__ == "__main__":
    global goal     # EatOur or TitanicSurvived ...
    global positive # True or 0 ...
    global negative 
    goal = "WillWait"
    positive = "Yes"
    negative = "No"
    first_line = ["Patrons", "Hungry", "Type", "Fri/Sat", "WaitEstimate", "Alternate", "Reservation", "Bar", "Raining"]

    ex_dict = {
        "Alternate": ["Yes", "Yes", "No", "Yes", "Yes", "No", "No", "No", "No", "Yes", "No", "Yes"],
        "Bar": ["No", "No", "Yes", "No", "No", "Yes", "Yes", "No", "Yes", "Yes", "No", "Yes"],
        "Fri/Sat": ["No", "No", "No", "Yes", "Yes", "No", "No", "No", "Yes", "Yes", "No", "Yes"],
        "Hungry": ["Yes", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes"],
        "Patrons": ["Some", "Full", "Some", "Full", "Full", "Some", "None", "Some", "Full", "Full", "None", "Full"], 
        "Raining": ["No", "No", "No", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "No", "No", "No"],
        "Reservation": ["Yes", "No", "No", "No", "Yes", "Yes", "No", "Yes", "No", "Yes", "No", "No"],
        "Type": ["French", "Thai", "Burger", "Thai", "French", "Italian", "Burger", "Thai", "Burger", "Italian", "Thai", "Burger"],
        "WaitEstimate": ["0-10", "30-60", "0-10", "10-30", ">60", "0-10", "0-10", "0-10", ">60", "10-30", "0-10", "30-60"],
        "WillWait": ["Yes", "No", "Yes", "Yes", "No", "Yes", "No", "Yes", "No", "No", "No", "Yes"]
    }
    examples = []
    for i in range(len(ex_dict["Alternate"])):
        example = dict()
        for key in ex_dict.keys():
            example[key] = ex_dict[key][i]
        examples.append(example)
    attributes = get_attributes_from_examples(examples, first_line)
    root = decision_tree_learning(attributes, examples, examples)
    bfs_print(root)
