# goal: organize given raw data and insert into tables
import pandas as pd


#-----------------------read raw data-------------------------------
# skip line 3350, 4704, 5879, 8981th row (not in the right format)
raw_data = pd.read_csv("books.csv", error_bad_lines=False)

# rename column
raw_data = raw_data.rename(columns={"  num_pages": "num_pages"})

# insert skipped records
skipped = pd.DataFrame({'bookID': [12224, 16914, 22128, 34889],
                        'title': ['Streetcar Suburbs: The Process of Growth in Boston, 1870-1900','The Tolkien Fan\'s Medieval Reader','Patriots (The Coming Collapse)', 'Brown\'s Star Atlas: Showing All The Bright Stars With Full Instructions How To Find And Use Them For Navigational Purposes And Department Of Trade Examinations.'],
                        'authors': ['Sam B. Warner, Jr.', 'David E. Smith/Verlyn Flieger','James Wesley Rawles','Brown Son & Ferguson Ltd.'],
                        'average_rating': [3.58, 3.58, 3.63, 0.00],
                        'isbn': ['674842111', '1593600119', '156384155X','851742718'],
                        'isbn13': ['9780674842113', '9781593600112', '9781563841552', '9780851742717'],
                        'language_code': ['en-US', 'eng','eng', 'eng'],
                        'num_pages': [236, 400, 342, 49],
                        'ratings_count': [61, 26, 38, 0],
                        'text_reviews_count': [6, 4, 4, 0],
                        'publication_date': ['4/20/2004', '4/6/2004','1/15/1999', '5/1/1977'],
                        'publisher': ['Harvard University Press', 'Cold Spring Press', 'Huntington House Publishers','Brown Son & Ferguson Ltd.']}) 

# merge two dataframes
books_data = raw_data.append(skipped, ignore_index=True) # skipped appended as last 4 rows (no duplicate indice)

#----------------make column "authors" atomic----------------
# turn authors column into a list
books_data['authors']= books_data['authors'].str.split("/")
# separate authors into rows that have one author per row
org_data = books_data.explode('authors', ignore_index=True) # make no duplicate indices

#----------------insert given  data into db-------------------
