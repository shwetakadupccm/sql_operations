import os
import sqlite3
import pandas as pd
import numpy as np
import itertools
import re
import pccm_db_curation.pccm_db_variable_dictonaries_sk as p_dict
from sqlalchemy import create_engine

# folder = 'D:/Shweta/pccm_db'
# file = 'PCCM_BreastCancerDB_2021_02_22.db'
#
# def get_data(folder, file, table_name):
#     path_db = os.path.join(folder, file)
#     conn = sqlite3.connect(path_db)
#     sql_stat = 'SELECT * FROM ' + table_name
#     df = pd.read_sql(sql_stat, conn)
#     return df
#
# dat = get_data(folder, file, 'patient_information_history')
#
# def get_value_from_key(vocab_dict, value):
#     id_pos = [value in value_list for value_list in (vocab_dict.values())]
#     key_reqd = list(itertools.compress(vocab_dict.keys(), id_pos))
#     return key_reqd
#
# key_reqd = get_value_from_key(physical_activity_dict, 'walked')
#
#
# def cleaned_and_get_key_value(defined_dict_variable, val):
#     split_val = val.split()
#     lst = []
#     for value in split_val:
#         cleaned_value = re.sub('[^a-zA-Z]', '', value)
#         cleaned_value = cleaned_value.lower()
#         key_reqd = get_value_from_key(defined_dict_variable, cleaned_value)
#         if key_reqd is not None:
#             key_reqd_str = '; '.join(key_reqd)
#             lst.append(key_reqd_str)
#             while ('' in lst):
#                 lst.remove('')
#         else:
#             lst.append(key_reqd)
#     return lst
#
# def replace_values_by_dict_keys(defined_dict_variable, df, variable_name):
#     variable_values = df[variable_name].str.lower()
#     dict_values = variable_values.to_dict()
#     changed_values = []
#     for val in dict_values.values():
#         if val is not None:
#             vocab_type = get_value_from_key(defined_dict_variable, val)
#             if len(vocab_type) != 0:
#                 changed_values.append(', '.join([str(elem) for elem in vocab_type]))
#             else:
#                 lst = cleaned_and_get_key_value(defined_dict_variable, val)
#                 changed_values.append(', '.join([str(elem) for elem in lst]))
#         else:
#             changed_values.append('data_not_available')
#     df[variable_name] = changed_values
#     df.replace(to_replace = '', value = 'data_to_be_curated', inplace = True)
#     return df, changed_values
#
#
# def curation_of_table(table_dat, curation_cols):
#     old_cols = table_dat.columns
#     for col in old_cols:
#         if col in curation_cols.keys():
#             defined_dict = p_dict.column_names_info(col)
#             replace_values_by_dict_keys(defined_dict, table_dat, col)
#     return table_dat
#
# curation_cols = {'type_physical_activity': 'physical_activity_dict',
#                  'diet': 'diet_dict',
#                  'menopause_status': 'menopause_status_dict',
#                  # 'age_at_menopause_yrs': 'age_at_menopause_yrs_dict',
#                  'current_breast_cancer_detected_by': 'current_breast_cancer_detected_by_dict',
#                  'lb_symptoms': 'rb_lb_symptoms_dict',
#                  'rb_symptoms': 'rb_lb_symptoms_dict',
#                  'patient_metastasis_symptoms': 'patient_metastasis_symptoms_dict'}
#
# def pccm_db_curation(folder, file):
#     path_db = os.path.join(folder, file)
#     conn = sqlite3.connect(path_db)
#     sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
#     tables = pd.read_sql(sql_stat, conn)
#     tabs = tables['name']
#     table_idx = [0, 4, 5, 15, 18, 20, 23]
#     engine = create_engine('sqlite:///D://Shweta//pccm_db//PCCM_BreastCancerDB_2021_02_22.db')
#     sqlite_connection = engine.connect()
#
#     for tab in tabs[table_idx]:
#         table_dat = get_data(folder, file, tab)
#         curation_cols = p_dict.curation_cols(tab)
#         curated_table = curation_of_table(table_dat, curation_cols)
#         sqlite_table = 'curated' + '_' + tab
#         curated_table.to_sql(sqlite_table, sqlite_connection, if_exists='fail')
#
# def data_to_be_curated(folder, file):
#     path_db = os.path.join(folder, file)
#     conn = sqlite3.connect(path_db)
#     sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
#     tables = pd.read_sql(sql_stat, conn)
#     tabs = tables['name']
#     table_idx = [25, 26, 27, 28, 29, 30, 31]
#
#     writer = pd.ExcelWriter('D:/Shweta/pccm_db/2021_05_30_pccm_db_data_to_be_curated_sk.xlsx',
#                             engine='xlsxwriter')
#
#     for tab in tabs[table_idx]:
#         tab_dat = pd.read_sql('SELECT * FROM' + ' ' + tab, conn)
#         tab_cols = tab_dat.columns
#         # print(tab_cols)
#         curation_dat_tab = pd.DataFrame()
#         for col in tab_cols:
#             col_dat = tab_dat[['file_number', col]]
#             # print(col_dat)
#             curation_dat = col_dat[col_dat[col] == 'data_to_be_curated']
#             # print(curation_dat)
#             if curation_dat.empty:
#                 continue
#             curation_dat_tab = pd.concat([curation_dat_tab, curation_dat], axis=1)
#         curation_dat_tab.to_excel(writer, sheet_name=tab[0:31], index=False)
#     writer.save()
#
# ## get_indexes
# patient_info = get_data(folder, file, 'patient_information_history')
# curated_patient_info = get_data(folder, file, 'curated_patient_information_history')
#
# def get_index_of_error_values(df, value='data_to_be_curated'):
#     positions = list()
#     result = df.isin([value])
#     series_obj = result.any()
#     col_names = list(series_obj[series_obj == True].index)
#     print(col_names)
#     for col in col_names:
#         rows = list(result[col][result[col] == True].index)
#         for row in rows:
#             positions.append((row, col))
#     return positions
#
# positions = get_index_of_error_values(curated_patient_info, 'data_to_be_curated')
#
# ##
#
# def get_error_values(old_df, positions_info_lst):
#     error_val_info = []
#     for positions_info in positions_info_lst:
#         index = positions_info[0]
#         col_name = positions_info[1]
#         col_dat = old_df.loc[:, col_name]
#         col_value = col_dat.iloc[index]
#         file_number = old_df['file_number']
#         file_number_error_val = file_number.iloc[index]
#         output_lst = np.append(col_name, col_value)
#         final_output_lst = np.append(file_number_error_val, output_lst)
#         error_val_info.append(final_output_lst)
#         output_df = pd.DataFrame(error_val_info, columns=['file_number', 'variable_name', 'error_value'])
#     return output_df
#
#
# df = get_error_values(patient_info, positions)
#
# ##
#
# def data_to_be_curated_df(folder, file):
#     path_db = os.path.join(folder, file)
#     conn = sqlite3.connect(path_db)
#     sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
#     tables = pd.read_sql(sql_stat, conn)
#     tabs = tables['name']
#     table_idx = [25, 26, 27, 28, 29, 30, 31]
#
#     writer = pd.ExcelWriter('D:/Shweta/pccm_db/output_df/2021_06_08_pccm_db_data_to_be_curated_sk.xlsx',
#                             engine='xlsxwriter')
#
#     df = pd.DataFrame(columns= ['file_number', 'variable_name', 'error_value', 'table_name'])
#     for tab in tabs[table_idx]:
#         curated_tab_dat = pd.read_sql('SELECT * FROM' + ' ' + tab, conn)
#         tab_name_str = tab[8:]
#         old_tab_dat = pd.read_sql('SELECT * FROM' + ' ' + tab_name_str, conn)
#         positions = get_index_of_error_values(curated_tab_dat, 'data_to_be_curated')
#         error_df = get_error_values(old_tab_dat, positions)
#         error_df_shape = error_df.shape
#         table_name = pd.Series(np.repeat(tab, error_df_shape[0]))
#         final_error_df = pd.concat([error_df, table_name], axis=1)
#         final_error_df.columns = ['file_number', 'variable_name', 'error_value', 'table_name']
#         df = pd.concat([df, final_error_df])
#         df = df.sort_values('file_number')
#         error_df.to_excel(writer, sheet_name=tab[0:31], index= False)
#     writer.save()
#     return df
#
# df = data_to_be_curated_df(folder, file)
# df.to_excel('D:/Shweta/pccm_db/output_df/2021_06_09_pccm_db_data_to_be_curated_info_sk.xlsx', index=False)
#
#
###

class PccmDbCuration:

    def __init__(self, folder, file):
        self.folder = folder
        self.file = file

    def get_data(self, table_name):
        path_db = os.path.join(self.folder, self.file)
        conn = sqlite3.connect(path_db)
        sql_stat = 'SELECT * FROM ' + table_name
        df = pd.read_sql(sql_stat, conn)
        return df

    @staticmethod
    def get_value_from_key(vocab_dict, value):
        id_pos = [value in value_list for value_list in (vocab_dict.values())]
        key_reqd = list(itertools.compress(vocab_dict.keys(), id_pos))
        return key_reqd

    @staticmethod
    def cleaned_and_get_key_value(defined_dict_variable, val):
        split_val = re.split(';|:|,| ', val)
        lst = []
        for value in split_val:
            cleaned_value = re.sub('[^a-zA-Z]', '', value)
            cleaned_value = cleaned_value.lower()
            key_reqd = self.get_value_from_key(defined_dict_variable, cleaned_value)
            if key_reqd is not None:
                key_reqd_str = '; '.join(key_reqd)
                lst.append(key_reqd_str)
                while ('' in lst):
                    lst.remove('')
            else:
                lst.append(key_reqd)
        return lst

    @staticmethod
    def replace_values_by_dict_keys(defined_dict_variable, df, variable_name):
        variable_values = df[variable_name].str.lower()
        dict_values = variable_values.to_dict()
        changed_values = []
        for val in dict_values.values():
            if val is not None:
                vocab_type = self.get_value_from_key(defined_dict_variable, val)
                if len(vocab_type) != 0:
                    changed_values.append(', '.join([str(elem) for elem in vocab_type]))
                else:
                    lst = self.cleaned_and_get_key_value(defined_dict_variable, val)
                    changed_values.append(', '.join([str(elem) for elem in lst]))
            else:
                changed_values.append('data_not_available')
        df[variable_name] = changed_values
        df.replace(to_replace='', value='data_to_be_curated', inplace=True)
        return df, changed_values

    @staticmethod
    def curation_of_table(table_dat, curation_cols):
        old_cols = table_dat.columns
        for col in old_cols:
            if col in curation_cols.keys():
                defined_dict = p_dict.column_names_info(col)
                self.replace_values_by_dict_keys(defined_dict, table_dat, col)
        return table_dat

    def pccm_db_curation(self):
        path_db = os.path.join(self.folder, self.file)
        conn = sqlite3.connect(path_db)
        sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
        tables = pd.read_sql(sql_stat, conn)
        tabs = tables['name']
        table_idx = [0, 4, 5, 15, 18, 20, 23]
        engine = create_engine('sqlite:///D://Shweta//pccm_db//PCCM_BreastCancerDB_2021_02_22.db')
        sqlite_connection = engine.connect()

        for tab in tabs[table_idx]:
            table_dat = self.get_data(self.folder, self.file, tab)
            curation_cols = p_dict.curation_cols(tab)
            curated_table = self.curation_of_table(table_dat, curation_cols)
            sqlite_table = 'curated' + '_' + tab
            curated_table.to_sql(sqlite_table, sqlite_connection, if_exists='fail')

    def drop_table(self):
        path_db = os.path.join(self.folder, self.file)
        conn = sqlite3.connect(path_db)
        sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
        tables = pd.read_sql(sql_stat, conn)
        tabs = tables['name']
        table_idx = [0, 4, 5, 15, 18, 20, 23]

        for tab in tabs[table_idx]:
            tab_name = 'curated' + '_' + tab
            print(tab_name)
            drop_stat = 'DROP TABLE' + ' ' + tab_name
            conn.execute(drop_stat)

    @staticmethod
    def get_index_of_error_values(df, value='data_to_be_curated'):
        positions = list()
        result = df.isin([value])
        series_obj = result.any()
        col_names = list(series_obj[series_obj == True].index)
        print(col_names)
        for col in col_names:
            rows = list(result[col][result[col] == True].index)
            for row in rows:
                positions.append((row, col))
        return positions

    @staticmethod
    def get_error_values(old_df, positions_info_lst):
        error_val_info = []
        for positions_info in positions_info_lst:
            index = positions_info[0]
            col_name = positions_info[1]
            col_dat = old_df.loc[:, col_name]
            col_value = col_dat.iloc[index]
            file_number = old_df['file_number']
            file_number_error_val = file_number.iloc[index]
            output_lst = np.append(col_name, col_value)
            final_output_lst = np.append(file_number_error_val, output_lst)
            error_val_info.append(final_output_lst)
            output_df = pd.DataFrame(error_val_info, columns=['file_number', 'variable_name', 'error_value'])
        return output_df

    def data_to_be_curated_df(self, value='data_to_be_curated'):
        path_db = os.path.join(self.folder, self.file)
        conn = sqlite3.connect(path_db)
        sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
        tables = pd.read_sql(sql_stat, conn)
        tabs = tables['name']
        table_idx = [25, 26, 27, 28, 29, 30, 31]

        writer = pd.ExcelWriter('D:/Shweta/pccm_db/output_df/2021_06_08_pccm_db_data_to_be_curated_sk.xlsx',
                                engine='xlsxwriter')

        df = pd.DataFrame(columns=['file_number', 'variable_name', 'error_value', 'table_name'])
        for tab in tabs[table_idx]:
            curated_tab_dat = pd.read_sql('SELECT * FROM' + ' ' + tab, conn)
            tab_name_str = tab[8:]
            old_tab_dat = pd.read_sql('SELECT * FROM' + ' ' + tab_name_str, conn)
            positions = self.get_index_of_error_values(curated_tab_dat, value)
            error_df = self.get_error_values(old_tab_dat, positions)
            error_df_shape = error_df.shape
            table_name = pd.Series(np.repeat(tab, error_df_shape[0]))
            final_error_df = pd.concat([error_df, table_name], axis=1)
            final_error_df.columns = ['file_number', 'variable_name', 'error_value', 'table_name']
            df = pd.concat([df, final_error_df])
            df = df.sort_values('file_number')
            error_df.to_excel(writer, sheet_name=tab[0:31], index=False)
        writer.save()
        return df
