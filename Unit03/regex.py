import re

text = ["The shoes cost $45, the shirt is $20, and the hat is $5.","$100"]

# The pattern: a literal dollar sign (\$), followed by one or more digits (\d+)
pattern = r"\$\d+" 

# Execute the search
for t in text:
    prices = re.findall(pattern, t)

    print(prices) 
# Output: ['$45', '$20', '$5']