CodePrinter: print code to pdf
### Example
1. Print *.py files
```
python demo.py -c path/to/your/code -f py
```
2. Print *.cpp  and *.py files
```
python demo.py -c path/to/your/code -f cpp,py
```
3. Use other style file in highlight/styles
```
python demo.py -c path/to/your/code -f py -s a11y-dark.css
```
You will get [Project].html [Project_content].txt
### Use GoogleChrome to open *.html and print it
![Google Chrome Printer(Ctrl+P)](config.png)