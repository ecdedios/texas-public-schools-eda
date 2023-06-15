# Texas Public Schools

> An exploratory data analysis of financial (PEIMS) and performace data (STAAR).

## Description

- What's money got to do with it?
- Which schools have the top performance scores?
- What financial profile is associated with high-performing schools?
- Are schools throwing allocating money effectively?

## Data Sources

- Financial Data
  - [2007-2021 Summarized PEIMS Actual Financial Data (Excel 17,185 KB)](https://tea.texas.gov/sites/default/files/2007-2021-summaried-peims-financial-data.xlsx)
  - [Parent Page](https://tea.texas.gov/finance-and-grants/state-funding/state-funding-reports-and-data/peims-financial-data-downloads)
  - [Data Dictionary](https://github.com/ecdedios/texas-public-schools/blob/main/docs/AbtAct21.docx)
- Academic Performance Data
  - [Texas Education Agency Data 2012-2019](https://www.kaggle.com/datasets/9e3ce42f60ded3ba2a6dd890993493f2c4b284c5cfa035d711bd98fa3359924c?resource=download)
- Educator Salary
  - [Staff Salary FTE Report Statewide Districts 2018-2019](https://rptsvr1.tea.texas.gov/adhocrpt/adpeb.html)

## Project Structure

- data
  - in - contains the original data sources
    - district-level financial data
    - campus-level academic performance data
  - inter - contains modified data
  - out - contains output report-ready data
- docs
  - data dictionary
  - PEIMS columns list
- notebooks
  - Texas Public Schools 01.ipynb - data acquisition and initial preparation
  - Texas Public Schools 02 - messy.ipynb - a rough look at the data
  - Texas Public Schools 02 - PEIMS.ipynb - expenditure data
  - Texas Public Schools 02 - STAAR.ipynb - district-level academic performance data
  - Texas Public Schools 03 - MASTERS COMBINED PEIMS AND STAAR.ipynb - merged data

## Limitations

I'm only looking at the 2019 or academic year 2018-2019.

## Meta

Ednalyn C. De Dios – [@ecdedios](https://github.com/ecdedios)

Distributed under the MIT license. See `LICENSE` for more information.

- LinkedIn: [in/ecdedios/](https://www.linkedin.com/in/ecdedios/)
- Resumé: [http://ednalyn.com](http://ednalyn.com)
- Data Science Projects [https://datasciencenerds.us](https://datasciencenerds.us)

## Contributing

1. Fork it (<https://github.com/ecdedios/texas-public-schools-eda/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
