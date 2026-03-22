To launch a Jupyter Notebook from your Windows Subsystem for Linux (WSL) terminal, follow these steps: 

1. Open your WSL terminal (e.g., Ubuntu). 
2. Navigate to your desired directory using the  command. To access your Windows file system, the path starts with . 
3. Ensure your Python environment is active (if using a virtual environment or Conda environment). 
4. Run the following command to start the Jupyter server: 
5. or, if the browser does not open automatically (common with some WSL configurations): 
6. Access the notebook in your Windows web browser. [1, 2, 3, 4, 5]  

Accessing the Notebook in your Windows Browser 
After running the command in step 4, the terminal will display output including a URL (usually ) and a security token. 

• If you ran , it should automatically open a new tab in your default Windows browser. 
• If you ran , you must copy and paste the full URL, including the token, into your web browser's address bar to access the notebook interface. [6, 11, 12]  

Optional: Automating the Browser Launch [13]  
If the browser doesn't open automatically with , you can configure it to use your Windows default browser by installing the  package within your Linux distribution, which provides the  command: 

• In your WSL terminal, run:  (for Debian-based distros like Ubuntu). 
• Add  to your  file to set  as the default browser. You can edit this file using . 
• After saving the file, close and reopen your WSL terminal for the changes to take effect. Now, running  should automatically open it in your Windows default browser. [14, 17, 18, 19, 20]  

AI can make mistakes, so double-check responses

[1] https://stackoverflow.com/questions/56347377/how-to-access-jupyter-notebook-stored-in-windows-when-jupyter-runs-from-ubuntu-w
[2] https://fintechpython.pages.oit.duke.edu/jupyternotebooks/0-Preliminaries/03-Windows_Installation.html
[3] https://code.visualstudio.com/docs/remote/wsl
[4] https://www.linkedin.com/pulse/how-bring-mac-like-terminal-windows-zsh-wsl-kamal-singh-y53ac
[5] https://ubuntu.com/desktop/wsl
[6] https://www.codecademy.com/article/how-to-use-jupyter-notebooks
[7] https://github.com/jupyter/notebook/discussions/7448
[8] https://harvardmed.atlassian.net/wiki/spaces/O2/pages/1594262530/Jupyter+on+O2
[9] https://www.bairesdev.com/blog/what-is-a-jupyter-notebook/
[10] https://linuxcapable.com/how-to-install-jupyter-notebook-on-ubuntu-linux/
[11] https://medium.com/data-science/configuring-jupyter-notebook-in-windows-subsystem-linux-wsl2-c757893e9d69
[12] https://saturncloud.io/blog/how-to-open-jupyter-notebook-in-chrome-on-windows/
[13] https://alexanderlabwhoi.github.io/post/2019-03-08_jpn-slurm/
[14] https://discourse.jupyter.org/t/issue-with-starting-jupyter-notebook-from-wsl/17441
[15] https://josedevezas.com/blog/jupyter_on_wsl/
[16] https://github.com/jupyter/notebook/issues/4594
[17] https://github.com/jupyter/notebook/issues/4594?timeline_page=1
[18] https://discourse.jupyter.org/t/issue-with-starting-jupyter-notebook-from-wsl/17441
[19] https://github.com/jupyter/notebook/issues/4594
[20] https://superuser.com/questions/1262977/open-browser-in-host-system-from-windows-subsystem-for-linux
