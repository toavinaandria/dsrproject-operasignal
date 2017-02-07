# README - Script to create a template txt file for manual annotation of rows to clean up and delete

for i in range(31):
    print('# df'+ str(i) + '.pkl' +'---------\n')
    print('rows_to_delete = []')
    print('custom_jobs = []')
    print('error_rows = []\n\n')