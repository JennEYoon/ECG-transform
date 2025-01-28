To untar a .tar.gz file in Python, you can use the tarfile module:   

```python
import tarfile

def untar_data(filename, extract_path="."):
    """Untars a .tar.gz file to the specified path."""

    with tarfile.open(filename, "r:gz") as tar:
        tar.extractall(path=extract_path)

# Example usage:
untar_data("my_data.tar.gz", "extracted_data")
```

Explanation: 

1. Import the tarfile module: This module provides functionality for working with tar archives. 
2. Define a function: The untar_data function takes the filename of the .tar.gz file and an optional extract_path argument to specify where to extract the contents. 
3. Open the tar archive: The tarfile.open() function opens the file in read mode with gzip compression ("r:gz"). 
4. Extract the contents: The extractall() method extracts all the members of the archive to the specified extract_path. 
5. Close the file: The with statement ensures the file is closed properly. 


Generative AI is experimental.

