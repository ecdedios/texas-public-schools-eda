import sys
import pandas as pd

def prep_staar(df1, df2):

    # Consolidate the two files into one dataframe
    df = pd.concat([df1, df2])


    # Get rid of duplciates
    df = df.drop_duplicates(keep='first')

    columns_to_drop = ['data_release',
                    'data_category',
                    'data_level',
                    'release_year'
                    ]

    # Get rid of unnecessary columns
    df.drop(columns=columns_to_drop, inplace=True)

    # Prepend with 0's
    df['campus_number'] = df['campus_number'].apply(lambda x: '{0:0>9}'.format(x))

    # Drop 'new_rate'
    df.drop(columns=['new_rate'], inplace=True)

    # Get the district number
    df['district'] = df['campus_number'].str[:6]

    # Turn dataset into district-level data
    df = df.groupby(['test_year',
                            'district',
                            'grade_level',
                            'subject',
                            'proficiency',
                            'demog'
                            ])[["numerator", "denominator"]].sum().reset_index()

    # Remove subsets
    df = df[df['grade_level'] == 'all']
    df = df[df['subject'] == 'all_subjects']
    df = df[df['demog'] == 'all_students']
    df = df.drop(columns=['grade_level',
                                'subject',
                                'demog'
                            ])

    # Create rate column
    df['rate'] = round(df['numerator'] / df['denominator'] * 100, 2)

    # Remove raw columns
    df = df.drop(columns=['numerator',
                                'denominator'
                            ])

    # Isolate 2019 test year
    df = df[df['test_year'] == 2019]
    df = df.drop(columns=['test_year'])

    df = df.rename(columns={'district':'District',
                            'proficiency':'Proficiency',
                            'rate':'Rate'
                            })

    print(df.shape)
    return df

def prep_peims(df):

    # Remove district name
    df = df.drop(columns=['DISTRICT NAME'])

    # Remove all columns between column name 'B' to 'D'
    df = df.drop(df.loc[:, 'GEN FUNDS-LOCAL TAX REVENUE FROM M&O':'ALL FUNDS-TOTAL OPERATING, OTR, DEBT SERV FIN, AND TRS EST REVEN'].columns, axis=1)

    # Isolate 2019 test year
    df = df[df['YEAR'] == 2019]
    df = df.drop(columns=['YEAR'])

    # Remove columns that starts with 'GEN'
    columns_to_keep = [c for c in df.columns if c.lower()[:3] != 'gen']
    df = df[columns_to_keep]

    # Remove Prefix 'all funds'
    df.columns = df.columns.str.replace("ALL FUNDS-", "")

    # Padd District numbers with 0's
    df['DISTRICT NUMBER'] = df['DISTRICT NUMBER'].str.zfill(6)

    # Remove all columns between column name 'B' to 'D'
    df = df.drop(df.loc[:, 'TOTAL OPERATING EXPENDITURES BY OBJ':'TOTAL NON-OPER AND OPER OEXPENDITURES BY OBJ'].columns, axis=1)
    df = df.drop(df.loc[:, 'TOTAL OPERATE EXPEND BY FUNCTION':'TOT OPER AND NON-OPER EXP BY FUNCTION'].columns, axis=1)
    df = df.drop(df.loc[:, 'TOTAL PROGRAM OPERATING EXPENDITURES':'EINTRAN4'].columns, axis=1)
    df = df.drop(df.loc[:, 'INTERGOVERN CHARGES EXPEND':'FALL SURVEY ENROLLMENT'].columns, axis=1)

    # Rename column
    df = df.rename(columns={'DISTRICT NUMBER':'DISTRICT'})

    # Remove word 'EXPENDITURES'
    df.columns = df.columns.str.replace("EXPENDITURES", "")

    # Remove word 'EXPEND'
    df.columns = df.columns.str.replace("EXPEND", "")

    # Remove word 'EXP'
    df.columns = df.columns.str.replace("EXP", "")

    # Remove word 'TOTAL'
    df.columns = df.columns.str.replace("TOTAL", "")

    # Remove word 'FCT'
    df.columns = df.columns.str.replace("FCT", "")

    # Remove dougble dashes
    df.columns = df.columns.str.replace("--", "-")

    # Remove double space opposite comma
    df.columns = df.columns.str.replace(" , ", ",")

    # Remove leading and treiling spaces
    df.columns = df.columns.str.strip()

    df = df.rename(columns={'DISTRICT':'District',
                            'PAYROLL':'Payroll',
                            'PROFESSIONAL & CONTRACTED SERVICES':'Professional & Contracted',
                            'SUPPLIES & MATERIALS':'Supplies & Materials',
                            'OTHER OPERATING':'Other Operating',
                            'INSTRUCTION + TRANSFER -11,95':'Instruction & Transfer',
                            'INSTRUC RESOURCE MEDIA SERVICE, 12':'Instructional Resource Media',
                            'CURRICULUM/STAFF DEVELOPMENT,13':'Curriculum/Staff Development',
                            'INSTRUC LEADERSHIP,21':'Instructional Leadership',
                            'CAMPUS ADMINISTRATION,23':'Campus Administration',
                            'GUIDANCE 7 COUNSELING SERVICES,31':'Guidance & Counseling',
                            'SOCIAL WORK SERVICES,32':'Social Work',
                            'HEALTH SERVICES,33':'Health Services',
                            'TRANSPORTATION,34':'Transportation',
                            'FOOD SERVICE,35':'Food Service',
                            'EXTRACURRICULAR ,36':'Extracurricular',
                            'GENERAL ADMINISTRAT -41,80,92':'General Administration',
                            'PLANT MAINTENANCE/OPERA,51':'Plant Maintenance/Operation',
                            'SECURITY/MONITORING SERVICE,5':'Security & Monitoring',
                            'DATA PROCESSING SERVICES, 53':'Data Processing',
                            'COMMUNITY SERVICES, 61':'Community Services',
                            'REGULAR PROGRAM -11':'Regular Program',
                            'GIFTED/TALENTED PROGRAM -21':'Gifted & Talented Program',
                            'CAREER & TECHNOLOGY PGM -22':'Career & Technology Program',
                            'STUDENTS WITH DISABILITIES PGM -23':'Students with Disabilities',
                            'STATE COMPENSATORY ED -24, 29, 30, 34':'State Compensatory Education',
                            'BILINGUAL PROGRAM -25':'Bilingual Program',
                            'HIGH SCHOOL ALLOTMENT PROGRAM-91':'High School Allotment',
                            'PREKINDERGARTEN-32,35':'Pre-K',
                            'PREKINDERGARTEN  BILINGUAL-32':'Pre-K Bilingual',
                            'PREKINDERGARTEN  COMP ED-32':'Pre-K Comp Ed',
                            'PREKINDERGARTEN  REGULAR-32':'Pre-K Regular',
                            'PREKINDERGARTEN  SPECIAL ED-32':'Pre-K Special Education',
                            'ATHLETICS PROGRAM-91':'Athletics Program',
                            'UNDISTRIBUTED PROGRAM -99':'Undistributed Program',
                            'OTHER USES':'Other Uses'
                            })

    df['District'] = df['District'].str[1:]
    
    print(df.shape)
    return df

def main():
    """Main entry point for the script."""

    # Get the PEIMS and STAAR datasets
    peims_df = pd.read_csv('../data/in/2007-2021-summaried-peims-financial-data.csv')
    staar_df1 = pd.read_csv('../data/in/tidy_campstaar1_2012to2019.csv')
    staar_df2 = pd.read_csv('../data/in/tidy_campstaar2_2013to2019.csv')

    staar = prep_staar(staar_df1, staar_df2)
    peims = prep_peims(peims_df)

    staar.to_csv('../data/inter/clean_staar_2019.csv', index=False)
    peims.to_csv('../data/inter/clean_peims_2019.csv', index=False)

if __name__ == '__main__':
    sys.exit(main())










__author__ = "Ednalyn C. De Dios, et al."
__copyright__ = "Copyright 2022, Texas Public School Project"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ednalyn C. De Dios"
__email__ = "ednalyn.dedios@gmail.com"
__status__ = "Prototype"