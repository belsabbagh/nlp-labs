import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def f(x, w, s):
    dot = np.dot(x, w)
    new_layer = np.full_like(x, dot)
    print("New Layer (before activation):", new_layer)
    new_layer = sigmoid(new_layer + np.sum(s))
    print("New Layer (after activation):", new_layer)
    s = new_layer
    final_output = sigmoid(np.sum(new_layer))
    print("Final Output:", final_output)
    return final_output, s

def evaluate_inputs(x, s):
    results = []
    for i, x_input in enumerate(x, start=1):
        print("\nEvaluating Input", i, ":", x_input)
        output, s = f(x_input.reshape(1, -1), [1, 1], s)
        results.append(output)
        print("Intermediate State after Input", i, ":", s)
    return results, s
  
if __name__ == "__main__":

  x_test = np.array([[1, 1], [1, 1], [2, 2]])
  s_test = np.array([0, 0])

  output, final_state = evaluate_inputs(x_test, s_test)

  print("\nFinal Results:", output)
  print("Final State:", final_state)
