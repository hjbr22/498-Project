import pandas as pd

def split_time_range(value):
    if pd.isna(value): 
        return pd.Series([None, None], index=['start', 'end'])
    if value in ['NONE', 'ALL']:
        return pd.Series([value, value], index=['start', 'end'])
    if ',' in str(value): 
        start, end = value.split(',', 1)
        return pd.Series([start.strip(), end.strip()], index=['start', 'end'])
    return pd.Series([value, value], index=['start', 'end'])

def get_parking_lots_single(df, time, parking_pass):
    pass_row = df[df.iloc[:, 0] == parking_pass]
    
    if pass_row.empty:
        return []
    
    available_lots = []
    for col in df.columns:
        if not (col.endswith('_start') or col.endswith('_end')):
            continue
        
        base_col = col.rsplit('_', 1)[0]
        
        start = pass_row[f'{base_col}_start'].values[0]
        end = pass_row[f'{base_col}_end'].values[0]
        
        if start == 'ALL' or end == 'ALL':
            available_lots.append(base_col) 
        elif start == 'NONE' or end == 'NONE':
            continue
        else:
            try:
                if (start == None) or (end == None):
                    continue
                start = int(start)
                end = int(end)
                if start <= time <= end:
                    available_lots.append(base_col) 
            except ValueError:
                continue 

    available_lots = list(set(available_lots))

    return available_lots

def get_parking_lots_main(excel_path, time, weekend_bool, parking_pass):
    weekday_times = pd.read_excel(excel_path, sheet_name="Weekday Times") 
    weekend_times = pd.read_excel(excel_path, sheet_name="Weekend Times") 

    if weekend_bool:
        weekend_times_split = pd.DataFrame()
        for col in weekend_times.columns:
            split_columns = weekend_times[col].apply(split_time_range)
            split_columns.columns = [f'{col}_start', f'{col}_end']
            weekend_times_split = pd.concat([weekend_times_split, split_columns], axis=1)
        return get_parking_lots_single(weekend_times_split, time, parking_pass)
    else:
        weekday_times_split = pd.DataFrame()
        for col in weekday_times.columns:
            split_columns = weekday_times[col].apply(split_time_range)
            split_columns.columns = [f'{col}_start', f'{col}_end']
            weekday_times_split = pd.concat([weekday_times_split, split_columns], axis=1)
        return get_parking_lots_single(weekday_times_split, time, parking_pass)