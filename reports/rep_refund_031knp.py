from db_oracle.connect import get_connection
import config as cfg
import xlsxwriter
import datetime
import os.path
from datetime import date, timedelta


# first = today.replace(day=1)


def rep_refund_031knp():
    now = datetime.datetime.now()
    # today = datetime.date.today()

    file_name = 'REFUND_031knp' + '.xlsx'
    file_path = cfg.REPORTS_PATH + file_name

    if os.path.isfile(file_path):
        return file_name
    else:
        con = get_connection()
        cursor = con.cursor()

    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 5)
    worksheet.set_column(1, 1, 12)
    worksheet.set_column(2, 2, 10)
    worksheet.set_column(3, 3, 12)
    worksheet.set_column(4, 4, 12)
    worksheet.set_column(5, 5, 12)
    worksheet.set_column(6, 6, 12)
    worksheet.set_column(7, 7, 12)
    worksheet.set_column(8, 8, 12)
    worksheet.set_column(9, 9, 12)
    worksheet.set_column(10, 10, 12)
    worksheet.set_column(11, 11, 12)
    worksheet.set_column(12, 12, 12)
    worksheet.set_column(13, 13, 12)
    worksheet.set_column(14, 14, 12)
    worksheet.set_column(15, 15, 12)
    worksheet.set_column(16, 16, 12)
    worksheet.set_column(17, 17, 12)

    print("Начало расчета за " + now.strftime("%d-%m-%Y %H:%M:%S"))

    # try:
    #	import cx_Oracle
    # except  ImportError:
    #	print ("Import Error:",info)
    #	exit()

    # if cx_Oracle.version<'7.3.0':
    #	print ("Very old version of cx_Oracle :",cx_Oracle.version)
    #	exit()

    # print ("Version cx_Oracle :",cx_Oracle.version)

    # con = cx_Oracle.connect(cfg.username, cfg.password, cfg.dsn, encoding=cfg.encoding)
    # cursor=con.cursor()

    print("DSN: " + str(con.dsn))
    print("Версия: " + con.version)

    print("\nНачинаем расчет: " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    cursor.execute("select rownum, a.sior_id, " +
                   "a.gfss_in_nom, " +
                   "to_char(a.doc_date,'dd.mm.yyyy'), " +
                   "a.p_bin, " +
                   "a.p_name, " +
                   "a.fio, " +
                   "a.iin, " +
                   "a.doc_ret, " +
                   "to_char(a.date_ret,'dd.mm.yyyy'), " +
                   "a.sum_gfss, " +
                   "a.period, " +
                   "to_char(a.date_ret_gk,'dd.mm.yyyy'), " +
                   "a.sum_ret_gk, " +
                   "a.doc_num_df, " +
                   "to_char(a.doc_date_df,'dd.mm.yyyy'), " +
                   "a.reason_return " +
                   "from HIST_RET_SO_031KNP a " +
                   "where a.deleted = 'N' ")

    print("Провели расчет и формируем Excel: " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    common_format = workbook.add_format({'align': 'center'})
    common_format.set_align('vcenter')
    common_format.set_text_wrap()
    sum_pay_format = workbook.add_format({'num_format': '#,###,##0.00', 'font_color': 'black', 'align': 'vcenter'})
    # date_format = workbook.add_format({'num_format':'dd/mm/yy', 'align': 'vcenter'})

    worksheet.write(0, 0, '№', common_format)
    worksheet.write(0, 1, '№ заявки', common_format)
    worksheet.write(0, 2, 'вх.№ письма ГК в ГФСС', common_format)
    worksheet.write(0, 3, 'Дата письма ГК в ГФСС', common_format)
    worksheet.write(0, 4, 'БИН плательщика', common_format)
    worksheet.write(0, 5, 'Наименование плательщика', common_format)
    worksheet.write(0, 6, 'ФИО участника СОСС', common_format)
    worksheet.write(0, 7, 'ИИН участника СОСС', common_format)
    worksheet.write(0, 8, 'Номер платежки отправки средств из ГФСС в ГК', common_format)
    worksheet.write(0, 9, 'Дата отправки средств из ГФСС в ГК', common_format)
    worksheet.write(0, 10, 'Сумма, переведенная  из ГФСС', common_format)
    worksheet.write(0, 11, 'Период', common_format)
    worksheet.write(0, 12, 'Дата поступления средств из  ГК в ГФСС', common_format)
    worksheet.write(0, 13, 'Сумма, переведенная в ГФСС из ГК', common_format)
    worksheet.write(0, 14, 'Номер письма Департамента Финансов', common_format)
    worksheet.write(0, 15, 'Дата письма Департамента Финансов', common_format)
    worksheet.write(0, 16, 'Причина возврата', common_format)

    row = 0
    for record in cursor:
        col = 0
        for list_val in record:
            if col < 17:
                worksheet.write(row + 1, col, list_val, common_format)
            if col == 17:
                worksheet.write(row + 1, col, list_val, sum_pay_format)
            col += 1
        row += 1
    # worksheet.write(row+1,3, "=SUM(D2:D"+str(row+1)+")",sum_pay_format)
    workbook.close()

    now = datetime.datetime.now()

    print("Завершен расчет: " + now.strftime("%d-%m-%Y %H:%M:%S"))

    con.commit()
    con.close()
    return file_name
