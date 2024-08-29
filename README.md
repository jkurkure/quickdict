# quickdict
Flexible dictionary lookup in Python. Requires the less pager which is included in Linux by default. It can be installed for Windows by running ```winget install jftuga.less``` from your command-line. 

## Examples
```python quickdict.py con 7``` will give you all the dictionary entries for words starting with "con—" with a minimum length of 7. The length argument can be omitted.
```python quickdict.py ing 5 <``` will give you the entries for all words ending with "—ing" with a minimum length of 5.
