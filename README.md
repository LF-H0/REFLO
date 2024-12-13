# DESCRIPTION:
a very accurate and fast tool that can find unfiltered/reflected characters on URLs that has parameters 

it helps bug bounty hunters and penetration testers to find unfiltered characters in URLs parameters

finding unfiltered characters can lead to other vulnerabilities like XSS and HTMLI and more




# INSTALLATION:

1 `git clone https://github.com/LF-H0/REFLO.git`

2 `cd REFLO`

3 `pip install -r requirements.txt`

4 `python3 REFLO.py -h`


# USAGE: 

## simple usage:

run REFLO against a file of urls containing parameters:

`python3 REFLO.py -i urls.txt`

## characters encoding:

encode characters by using URL encoding before sending the requests:

`python3 REFLO.py -i urls.txt -e`

## output file:

save results to a txt file:

`python3 REFLO.py -i urls.txt -o`
