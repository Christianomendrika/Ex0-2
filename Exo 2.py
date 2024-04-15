from itertools import product

def generate_truth_table(expression):
    variables = sorted(set(expression.replace('(', '').replace(')', '').replace('+', '').replace('*', '')))

    table = []
    for values in product([0, 1], repeat=len(variables)):
        value_dict = dict(zip(variables, values))
        eval_result = eval(expression, value_dict)
        row = [value_dict[var] for var in variables] + [eval_result]
        table.append(row)

    return table, variables

def karnaugh_map(table, variables):
    n_variables = len(variables)
    n_rows = 2 ** n_variables
    n_cols = n_variables
    k_map = [['-' for _ in range(n_cols)] for _ in range(n_rows)]

    for i, row in enumerate(table):
        if row[-1] == 1:
            indices = [row[:-1]]
            for j in range(n_variables):
                temp_indices = []
                for index in indices:
                    index_copy = index.copy()
                    index_copy[j] = '-'
                    temp_indices.append(index_copy)
                indices.extend(temp_indices)
            for index in indices:
                k_map[index[0]][index[1]] = '1'

    return k_map

def simplify_k_map(k_map, variables):
    groups = []

    # Find horizontal groups
    for i in range(len(k_map)):
        group = []
        for j in range(len(k_map[i])):
            if k_map[i][j] == '1':
                group.append((i, j))
            else:
                if group:
                    groups.append(group)
                    group = []
        if group:
            groups.append(group)

    # Find vertical groups
    for j in range(len(k_map[0])):
        group = []
        for i in range(len(k_map)):
            if k_map[i][j] == '1':
                group.append((i, j))
            else:
                if group:
                    groups.append(group)
                    group = []
        if group:
            groups.append(group)

    # Simplify groups
    simplified_terms = set()
    for group in groups:
        if len(group) == 1:
            row, col = group[0]
            simplified_terms.add(variables[row] + "'" * (col == 0) + "'" * (col == 1))
        else:
            row_diff = group[-1][0] - group[0][0]
            col_diff = group[-1][1] - group[0][1]
            if row_diff == 0:
                simplified_terms.add(variables[group[0][0]] + "'" * (group[0][1] == 0) + "'" * (group[0][1] == 1))
            elif col_diff == 0:
                simplified_terms.add(variables[group[0][1]] + "'" * (group[0][0] == 0) + "'" * (group[0][0] == 1))

    return simplified_terms

if __name__ == "__main__":
    expression = input("Entrez une expression logique en utilisant les opérateurs *, + et ~ pour la négation : ")

    table, variables = generate_truth_table(expression)
    k_map = karnaugh_map(table, variables)

    print("\nKarnaugh Map:")
    for row in k_map:
        print(" ".join(row))

    simplified_terms = simplify_k_map(k_map, variables)
    print("\nExpression simplifiée:")
    print(" + ".join(simplified_terms))
