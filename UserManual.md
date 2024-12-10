# User Manual

## Setting Up for the First Time

1. **Install AlvaDesk Software**  
   Download and install [AlvaDesk Software](https://www.alvascience.com/alvadesc/).

2. **Install the AlvaDesc Python Wrapper**  
   Follow the instructions in [this video tutorial](https://www.youtube.com/watch?v=8yoIiO4A5zY&t=53s).  
   **Note:** The AlvaDesk Software must be installed beforehand, and you must have a valid license.

3. **Check and Install Dependencies**  
   Ensure all required dependencies are installed on your device:  
   - Dependencies are listed in the `Pipfile` or can be found in the **Insights** section on GitHub repository.  
   - To verify installed dependencies, run the following command in your terminal:  
     ```bash
     pip3 list
     ```  
     or  
     ```bash
     pip list
     ```  
     This will display a list of all Python packages currently installed.  

   - If any dependency is missing, install it using the following command:  
     ```bash
     pip3 install <dependency_name>
     ```  
     or  
     ```bash
     pip install <dependency_name>
     ```

4. **Proceed to the "Running the Script" Section**  
   Once the setup is complete, follow the instructions in the next section.

---

## Running the Script

1. **Configure the Script**  
   Open the `/Scripts/config.ini` file and update the variables to suit your requirements.

2. **Navigate to the Scripts Directory**  
   The code must be executed from the `/Scripts` directory. Use the `cd` command in your terminal to navigate to this directory:  
   ```bash
   cd <Path_to_the_repository>/Scripts
   ```  
3. **Compile the code**
   Run `python3 Main.py` or `python Main.py` in the terminal.
   ```bash
   python3 Main.py 
   ```  
   or 
   ```bash
   python Main.py 
   ```  
   in the terminal.

---

## Do you need more help?

Do not hesitate to comment on the **Issues** or **Discussion** GitHub sections. Additionally you can also contact **Me** (Contacts.md file).   
