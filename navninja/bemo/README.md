
```bash
datestamp=$(date +"%y%m%d")
wget https://documents.barings.com/docs/barings-emerging-emea-opportunities-plc-portfolio-holdings-en.pdf -O bemo-portfolio-holdings-${datestamp}.pdf
```

Copy the text from the pdf to a txt file. Delete the header row