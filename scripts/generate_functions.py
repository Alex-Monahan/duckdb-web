import duckdb
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 1000)
import io
import os

conn = duckdb.connect(':memory:')
# output_df = conn.execute("""
#     select
#         *
#     from duckdb_functions()
# """).fetchdf()
# output_df.to_csv('duckdb_functions.tab',sep='\t', index=False)

# output_df = conn.execute(r"""
#      --create view docs as
#      select * from read_csv_auto('./_data/existing_function_documentation.txt', delim='\t', header=True, all_varchar=True)
#      where description like '%Pattern%'
# """).fetchdf()

# output_df = conn.execute(r"""
#     select * from pragma_table_info('test_import')
# """).fetchdf()

# print(output_df.to_string())
def parse_markdown_tables(filepath):
    """Search through filename for Markdown tables (look for |:---|). Return a Pandas DataFrame of contents plus filepath and header name."""

    with open(filepath,'r',encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    print(lines[:10])

    #TODO: Once a table line is found, grab the prior line as headers
    #Save off the tables / parse them into Pandas in some way (not sure how to handle || operator, maybe just skip lines that don't have the same number of columns as the header)
    #Check for a header on each line. Use that header as a column in the dataset. Also include the filepath / filename
    within_table = False
    tables = []
    current_header=''
    for i, line in enumerate(lines):
        if len(line) > 0 and line.strip(' ')[0] == '#':
            current_header = line.strip('#').strip(' ')
            print('current_header:',current_header)
        if '|:---|' in line:
            print('Found a table!','\n',i,line)
            within_table = True
            tables.append(['| '+'filepath'+' | '+'current_header' + lines[i-1]])
            continue #Don't save that line
        if line == '':
            if within_table:
                print('End of table')
            within_table = False
        if within_table:
            print('Within table, line',i)
            tables[-1].append('| '+filepath+' | '+current_header + line)
        else:
            print('not in table, line',i)
    print(tables)
    df_list = []
    for table in tables:
        my_stringio = io.StringIO()
        for line in table:
            my_stringio.write(line.strip('|').strip(' '))
            # my_stringio.write(line)
            my_stringio.write('\n')
        my_stringio.seek(0)
        # print(my_stringio.getvalue())
        df = pd.read_table(my_stringio,sep='|',engine='python',on_bad_lines='warn',skiprows=[1])
        df.columns = [col.strip(' ') for col in df.columns.tolist()]
        df_list.append(df)
    if len(df_list) == 0:
        return pd.DataFrame()
    else:
        return pd.concat(df_list,axis='index',ignore_index=True)

# filepath = r'docs\sql\functions\char.md'
# filepath = r'docs\sql\functions\nested.md'
# output_df = parse_markdown_tables(filepath)
# print(output_df.head())
# output_df.to_csv(filepath.replace('.md','.txt'),sep='\t')
 
# iterate over files in
# that directory
md_dfs = []
for root, dirs, files in os.walk(r'docs\sql\functions'):
    for filename in files:
        print(os.path.join(root, filename))
        md_dfs.append(parse_markdown_tables(os.path.join(root, filename)))

all_files_md = pd.concat(md_dfs,axis='index',ignore_index=True)
print(all_files_md.head())
all_files_md.to_csv(r'docs\sql\functions\descriptions.txt',sep='\t',index=False)