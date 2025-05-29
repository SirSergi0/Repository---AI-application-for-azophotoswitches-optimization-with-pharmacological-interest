# Repository: AI Application for Azophotoswitches Optimization with Pharmacological Interest
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.txt) 
[![DOI](https://zenodo.org/badge/744140153.svg)](https://doi.org/10.5281/ZENODO.15546443)
[![ORCID](https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png)](https://orcid.org/0009-0007-7784-5537)

[![Creator: MolBioMed](https://webs.uab.cat/molbiomed/wp-content/uploads/sites/355/2023/03/logo_psi_redim.png)](https://webs.uab.cat/molbiomed/en/) 

In this work, we propose the development of specialized software in the field of artificial intelligence (AI), designed specifically for the discovery and optimization of azophotoswitches. Azophotoswitches are molecules that can undergo reversible changes in structure and function in response to light, making them valuable in applications ranging from molecular devices to advanced materials and medical therapies.

The proposed AI-driven software will leverage cutting-edge machine learning algorithms and data-driven techniques to facilitate the identification and prediction of new azophotoswitches with desired properties. By analyzing vast datasets of molecular structures, photochemical behaviors, and functional performance, the AI system aims to streamline the traditionally labor-intensive process of discovering these compounds. This approach will not only enhance the efficiency of the research but also expand the possibilities for designing azophotoswitches with novel functionalities, opening up new pathways in materials science and photopharmacology.

## License and Creator

This project is crated by [Sergio Castañerias Morales](mailto:sergiocastaneirasmorales@gmail.com) under the supervision of the research group [MolBioMed](https://webs.uab.cat/molbiomed/en/).

This project is licensed under the **GNU General Public License v3.0**. You may copy, distribute, and modify the software as long as you track changes/dates in source files and license all derivative works under the same license.

## Comments and Features of the Project

Comments will be added throughout the project's development. This list may not be updated regularly.

### UserGuide.md 
- File containing a User-Guide for helping with the implementation of the repository to a device.
- It is hardly recommended to consult this text at least once.

### General Guidelines

- For any problems or questions, please use the **_Issues_** and **_Discussions_** sections.
- To maintain order and organization, visitors are requested to locate all requests, inquiries, and issues in the appropriate sections.

### Diary

- The file called `Diary.md` will be the roadmap for the project. This file will keep track of all the main appointments and meetings of the project. Also the key point of each event will be stored there within a little summary of each discussion.
- This file will always be on the main repository location and will have regular updates.

### Contacts

- The file `Contacts.md` will ramain in the main repository location and will store all the general contact information related to the project.

### Notes

- The directory `Notes` will contain all the definitions, observations and reflections uppon the project. 
- The information is located in the `Notes/notes.pdf` file, which will be some sore of *Wikipedia* for the project, storing all the relevant data.
- All references are located in the `Notes/references.bib` file. This file will keep track of every single file consultated.

### Scripts

- The directory `Scripts` will contail all the scripts of this project. 
- Additionally, it will also contain a file `Scripts/READMEScripts.md` where a short description of each script will be stored.

### Manuscript

- The manuscript in PDF format will always be placed in the `Manuscript` directory and will be named `manuscript.pdf`.
- This directory also contains a `references.bib`. Although not all references may appear in the final manuscript, they will be stored there to keep track of all consulted files, books, websites, etc.

### Pipfile
- The only porpuse of this file is pointing out at the dependencies of the project. This information is nicely displaced at the `Insights/Dependency Graph` section. 
- **It is highly recomended** to consult the dependencies before runing the code. Otherwise, the most probable output will be an error message.

### Data 
- Directory incharged of storing all the data (eather raw data extracted from a database or computed data with chemical descriptors as well).

### Predictions
- Directory that will contain all the predictions provided by the AI.

### Avogadro Frames
- This directory contains the Avogadro files for the azophotoswitches. The primary purpose of these files is to obtain the SMILES representation of each azophotoswitch.

### SMILES Files
- This directory stores the SMILES strings of the azophotoswitches. A script from the scripts directory uses these files to predict the $IC_{50}$ values for each azophotoswitch.

### Machine Learning Models
- This directory contains all the generated machine learning models. Each model is saved as a [pickle files](https://docs.python.org/3/library/pickle.html) named according to the variables used to create it. Alongside each pickle file is a corresponding text file with the same name, providing additional information about the model.
