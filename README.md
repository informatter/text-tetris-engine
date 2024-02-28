# A simple text based tetris engine

The program which takes as input through the CLI a string encoding polyminoe's and their location on the board.

The following supported pieces are Q, S, Z, I, L, J and T. 

<table>
   <tbody><tr>
     <td>Letter</td>
     <td>Q</td>
     <td>Z</td>
     <td>S</td>
     <td>T</td>
     <td>I</td>
     <td>L</td>
     <td>J</td>
   </tr>
   <tr>
     <td>Polyminoe</td>
     <td>
       <pre> ##
 ##
       </pre>
     </td>
     <td>
       <pre> ##
  ##
       </pre>
     </td>
     <td>
       <pre>  ##
 ##
       </pre>
     </td>
     <td>
       <pre> ###
  #
       </pre>
     </td>
     <td>
       <pre> ####
       </pre>
     </td>
     <td>
       <pre> #
 #
 ##
       </pre>
     </td>
     <td>
       <pre>  #
  #
 ##
       </pre>
     </td>
   </tr>
 </tbody></table>

 The input is provided as a string like:  'Q0,Q1'
 The integers correspond to the left most column the polyminoe should be placed at.

Built against python 3.11.7 🐍


## Running the engine

### Install dependencies
The solution uses the following dependencies:
- pytest
- numpy
- pyinstaller

### Create virtual environment

`python -m venv env`

### Activate virtual environment

Windows 🪟

`env/scripts/activate.ps1`

macOS 🍎 / Linux 🐧

`source env/bin/activate`

### Install dependencies

`pip install -r requirements.txt`

### Run solver

`python tetris.py 'Q0,Q2'`

Use `--help for more options`

# Run tests 🧪

**Solver:**

`pytest tests/tetris_solver_tests.py`

**Polyminoe factory:**

`pytest tests/factory_test.py`
