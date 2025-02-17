# Where to store notebooks used in wiki 

Q.) 
When using the wiki section of Github repo, how should I organize the notebooks used in the wiki? Should I copy the final notebook into a new "notebooks" folder inside wiki or keep the notebook in the repo root subfolder "notebooks" and add link in the wiki documentation?

A.) 
The best approach is to **keep the notebooks in the main repository's `notebooks/` folder** and link to them in the Wiki documentation. Here’s why:  

### ✅ **Advantages of Keeping Notebooks in the Main Repo (`notebooks/` folder)**  
1. **Version Control**: Notebooks in the main repo are tracked with Git, whereas the Wiki is a separate Git repository. Keeping notebooks in the repo ensures better versioning.  
2. **Direct Execution**: Users can download, modify, and run the notebooks directly.  
3. **Avoid Duplication**: Copying the final notebook into the Wiki can lead to inconsistencies if updates are made in the main repo.  

---

### **🔗 How to Link Jupyter Notebooks in the Wiki**  

#### **1️⃣ Link to a Notebook in the Main Repo**  
Use the raw GitHub URL in your Wiki:  
```md
[ECG Signal Processing Notebook](https://github.com/your-username/your-repo/blob/main/notebooks/ecg_processing.ipynb)
```
🔹 **Pros:** Always links to the latest version of the notebook in the repo.  

---

#### **2️⃣ Embed a Notebook as a Static HTML Preview**  
Use [nbviewer](https://nbviewer.org/) to render a readable preview:  
```md
[View ECG Processing Notebook](https://nbviewer.org/github/your-username/your-repo/blob/main/notebooks/ecg_processing.ipynb)
```
🔹 **Pros:** This makes it easier to read notebooks without downloading.  

---

#### **3️⃣ Add Screenshots or Export as Markdown**  
For better readability in the Wiki, you can:  
- **Take a screenshot** of key results and embed them:  
  ```md
  ![ECG Feature Extraction](https://github.com/your-username/your-repo/blob/main/images/ecg_features.png)
  ```
- **Export key notebook cells as Markdown** and include them in the Wiki for explanation.  

---

### ❌ **When to Copy Notebooks into the Wiki?**  
Only if:  
- You want a **static, read-only version** of a finalized notebook.  
- The notebook contains **documentation-style explanations** instead of code-heavy sections.  

Even in these cases, I’d recommend **exporting to Markdown or HTML** instead of copying `.ipynb` files into the Wiki.

---

### **🔹 Recommended Approach:**  
📂 **Keep notebooks in `notebooks/` and link them in the Wiki** using GitHub or nbviewer.  

Would you like a specific example of a linked notebook with rendered visuals? 🚀

