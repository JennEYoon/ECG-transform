# How to remove singleton axis, using arr.squeeze(axis= )

# Assuming your original array is 'arr'
arr = np.random.rand(9308, 1, 186)  # Example array with shape (9308, 1, 186)

# Remove the second dimension (axis 1)
arr_squeezed = arr.squeeze(axis=1)

print(arr_squeezed.shape)  # Output will be (9308, 186)

