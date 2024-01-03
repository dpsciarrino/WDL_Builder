# WDL Builder

WDL Builder is a third-party tool for generating WDL files for AutoCAD Electrical projects.

Anyone who has worked with AutoCAD Electrical template blocks has learned that WDL files are usually written by hand in a text editor such as Notepad.

WDL Builder seeks to add a GUI interface for writing WDL files.

## Features (v0.1)

- Easily open and edit existing WDL file "Line" descriptions.
- Create new WDL files.
- Add/Modify/Remove lines from a WDL file.

## Running WDL Builder

1. Download Python 3.12.0
2. Download git.
3. Clone this repository with the following line:

```
git clone https://github.com/dpsciarrino/WDL_Builder.git
```

4. Navigate to the directory where you cloned the repository.
5. Run the following Python command in the same directory as the run.py file:

```
python run.py
```

Alternatively, you can opt to create an exe file. First, download pyinstaller with:
```
pip install pyinstaller
```

Then, run the following command:
```
pyinstaller --onefile --noconsole run.py
```

You will find the .exe file in the dist folder.