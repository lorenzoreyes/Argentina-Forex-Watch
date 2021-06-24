import urllib.request
import pandas as pd
import datetime as dt 
import yfinance as yahoo
import matplotlib.pyplot as plt 
from pylab import mpl
mpl.rcParams['font.family'] = 'serif'
plt.style.use('fivethirtyeight')

today = dt.date.today()

url = 'https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/seriese.xls'
u = urllib.request.urlretrieve(url, 'seriese.xls')

# Sheetnames of seriese.xls available at the link url
# ['BASE MONETARIA', 'RESERVAS','DEPOSITOS','PRESTAMOS','TASAS DE MERCADO',
# 'INSTRUMENTOS DEL BCRA', 'NOTAS']
# download the sheets and clean the data
basem = pd.read_excel(u[0], sheet_name='BASE MONETARIA')
reservas = pd.read_excel(u[0], sheet_name='RESERVAS')
depositos = pd.read_excel(u[0], sheet_name='DEPOSITOS')
#prestamos = pd.read_excel(u[0], sheet_name='PRESTAMOS')
#tasas = pd.read_excel(u[0], sheet_name='TASAS DE MERCADO')
instrumentos = pd.read_excel(u[0], sheet_name='INSTRUMENTOS DEL BCRA')
#notas = pd.read_excel(u[0], sheet_name='NOTAS')

# iloc[8:-243] only rows needed, outside of this range is not relevant
monetaria = pd.DataFrame(basem.iloc[8:-243,24].values,columns=['billete_publico'],index=basem.iloc[8:-243,0].values)
monetaria = monetaria.iloc[:-2,:]
# in order to have all the same range of data define start and end dates
start = dt.datetime(2019,1,1)
start_date = monetaria.loc[start:].head(1).index.values[0]
end_date = monetaria.index[-1]

# Take every monetary aggregate
depositos = depositos.iloc[5:-456,:]
#fechas = basem.iloc[8:-43,0] 
monetaria['billete_privado'] = basem.iloc[8:-245,25].values
monetaria['circulante'] = monetaria['billete_publico'] + monetaria['billete_privado']
monetaria['cta_cte_bcra'] = basem.iloc[8:-245,27].values
monetaria['total_base'] = monetaria['billete_privado'] + monetaria['billete_publico'] + monetaria['cta_cte_bcra']
monetaria = monetaria.loc[start_date:end_date]
length = len(monetaria) # extent of how long the series you want it to be. global variable 
herramientas = pd.DataFrame(instrumentos.iloc[8:-11,1].values,columns=['pases'],index=instrumentos.iloc[8:-11,0].values)
herramientas['leliqs'] = instrumentos.iloc[8:-11,4].values
herramientas['legar'] = instrumentos.iloc[8:-11,5].values
reservorio = pd.DataFrame(reservas.iloc[10:-254,3].values,columns=['stock_reservas'],index=reservas.iloc[10:-254,0].values)
reservorio['tc_oficial'] = reservas.iloc[10:-254,-1].values
indice = []
for i in range(len(reservorio.index)):
  indice.append(dt.datetime.strptime(str(reservorio.index.values[i])[0:10],'%Y-%m-%d'))
reservorio.index = indice 
herramientas,reservorio = herramientas.loc[start_date:end_date],reservorio.loc[start_date:end_date]
monetaria['pases'] = herramientas.pases.values
monetaria['leliqs'] = herramientas.leliqs.values
monetaria['legar'] = herramientas.legar.values
monetaria['stock_reservas'] = reservorio.stock_reservas.values

depositos = depositos.iloc[:-4,:]
depositado = pd.DataFrame(depositos.iloc[:,1].values,columns=['cta_ctes_publico'],index=depositos.iloc[:,0].values)
depositado['cta_ctes_privado'] = depositos.iloc[:,10].values
depositado['caja_ahorro'] = depositos.iloc[:,11].values
depositado['plazos_tres'] = (depositos.iloc[:,12].values + depositos.iloc[:,13].values + depositos.iloc[:,14].values)
depositado['total_depositos_publico'] = depositos.iloc[:,11].values
depositado['total_depositos_privado'] = depositos.iloc[:,18].values
depositado['M2'] = depositos.iloc[:,-1].values
depositado = depositado.tail(length) #.loc[start_date:end_date]
monetaria['cta_ctes_publico'] = depositado.cta_ctes_publico.values
monetaria['cta_ctes_privado'] = depositado.cta_ctes_privado.values
monetaria['M1_circulante_y_ctasctespublicas'] = monetaria['circulante'] + monetaria['cta_ctes_publico']
monetaria['caja_ahorro'] = depositado.caja_ahorro.values
monetaria['plazos_tres'] = depositado.plazos_tres.values
monetaria['total_depositos_publico'] = depositado.total_depositos_publico.values
monetaria['total_depositos_privado'] = depositado.total_depositos_privado.values
monetaria['M2'] = depositado.M2.values
monetaria['M3'] = (monetaria['billete_publico'] + monetaria['billete_privado'] + monetaria['total_depositos_privado']) / monetaria['stock_reservas']
monetaria['TC Oficial'] = reservorio.tc_oficial.tail(length).values
monetaria['SOLIDARIO'] = reservorio.tc_oficial.tail(length).values * 1.30 * 1.35
aapl = yahoo.download("AAPL AAPL.BA",start=start_date,end=end_date)['Adj Close'].fillna(method="ffill")
aapl = aapl.rename(columns={'AAPL.BA':'AAPLBA'})
tcaapl = (aapl.AAPLBA / aapl.AAPL) * 10
tcaapl = tcaapl.tail(len(monetaria))
monetaria['CCL AAPLBA'] = tcaapl.values
monetaria = monetaria.fillna(value=0.0)
monetaria['FX Fundamental'] = (monetaria['pases'] + monetaria['leliqs'] + monetaria['legar'] + monetaria['total_base']) / monetaria['stock_reservas']
monetaria['Monetarista Blue'] = monetaria['TC Oficial'] * (1 + (-monetaria['total_base'].pct_change().cumsum() + monetaria['CCL AAPLBA'].pct_change().cumsum()))
monetaria['Brecha'] = (monetaria['CCL AAPLBA'] / monetaria['TC Oficial']) - 1.0
monetaria = monetaria.fillna(method='ffill')
monetaria = round(monetaria,2)

# translate columns to english
monetaria = monetaria.rename(columns={'billete_publico':'public_coin','billete_privado':'private_coin','circulante':'supply',\
                                      'cta_cte_bcra':'bcra_current_account','pases':'bank_passes','stock_reservas':'reserves_stock',\
                                          'cta_ctes_publico':'public_current_accounts','cta_ctes_privado':'private_current_accounts','M1_circulante_y_ctasctespublicas':'M1',\
                                              'caja_ahorro':'saving_accounts','plazo_tres':'fixed_term','total_depositos_publico':'total_public_deposits','total_depositos_privado':'total_private_deposits',\
                                                  'M2':'M2','M3':'M3','TC Oficial':'Official_Exchange_Rate','SOLIDARIO':'SOLIDARITY','FX Fundamental':'Fundamental Forex','Monetarista Blue':'Monetary Vision',\
                                                      'Brecha':'GAP'})

# Add last price in the colums so the plot appear in legend too 
monetaria = monetaria.rename(columns={'M3':f'M3 ${monetaria["M3"].tail(1).values[0]}'})
monetaria = monetaria.rename(columns={'Monetary Vision':f'Monetary Vision ${monetaria["Monetary Vision"].tail(1).values[0]}'})
monetaria = monetaria.rename(columns={'CCL AAPLBA':f'CCL AAPLBA ${monetaria["CCL AAPLBA"].tail(1).values[0]}'})
monetaria = monetaria.rename(columns={'Fundamental Forex':f'Fundamental Forex ${monetaria["Fundamental Forex"].tail(1).values[0]}'})
monetaria = monetaria.rename(columns={'GAP':f'GAP {monetaria["GAP"].tail(1).values[0] * 100}%'})
monetaria = monetaria.rename(columns={'Official_Exchange_Rate':f'Official_Exchange_Rate ${monetaria["Official_Exchange_Rate"].tail(1).values[0]}'})
monetaria = monetaria.rename(columns={'SOLIDARITY':f'SOLIDARITY ${monetaria["SOLIDARITY"].tail(1).values[0]}'})

# Final plots
fig = plt.figure(figsize=(50,25))
ax1 = fig.add_subplot(111)
monetaria.iloc[:,-6:-1].plot(ax=ax1, lw=10.)
ax1.set_title('Argentina Forex Spectrum', fontsize=120, fontweight='bold')
ax1.grid(linewidth=2)
ax1.legend(loc='best', bbox_to_anchor=(1., 0.85),fontsize=100)
plt.xticks(size = 80)
plt.yticks(size = 80)
plt.savefig('ArgentinaFX.png',bbox_inches='tight')

figb = plt.figure(figsize=(50,25))
ax1 = figb.add_subplot(111)
monetaria.iloc[:,-1].plot(ax=ax1, lw=7.)
ax1.set_title('GAP CCL AAPLBA vs. Official', fontsize=120, fontweight='bold')
ax1.grid(linewidth=2)
ax1.legend(loc='best', bbox_to_anchor=(1., 0.85),fontsize=100)
plt.xticks(size = 80)
plt.yticks(size = 80)
plt.savefig('gap.png',bbox_inches='tight')

# save the excel
writer = pd.ExcelWriter(f'Central Bank Report {today}.xlsx',engine='xlsxwriter')
monetaria.to_excel(writer,sheet_name=f'report {today}')
writer.save()
