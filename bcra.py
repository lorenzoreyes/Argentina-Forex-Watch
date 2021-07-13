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
#notas = pd.read_excel(u[0], sheet_name='NOTAS')import urllib.request
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
#notas = pd.read_excel(u[0], sheet_name='NOTAS'

discardBASEM = []
for i in range(len(basem)):
    if type(basem.iloc[i,0]) != type(basem.iloc[8,0]):
        discardBASEM.append(i)
    else:
        pass
        
interval = [(max(discardBASEM[:8]))+1,min(discardBASEM[8:])]
basem = basem.iloc[interval[0]:interval[1]]
monetaria = pd.DataFrame(basem.iloc[:,24].values,columns=['billete_publico'],index=basem.iloc[:,0].values)
start = dt.datetime(2020,1,1)
start_date = monetaria.loc[start:].head(1).index.values[0]
end_date = monetaria.index[-1]

# Take every monetary aggregate
monetaria['billete_privado'] = basem.iloc[:,25].values
monetaria['circulante'] = monetaria['billete_publico'] + monetaria['billete_privado']
monetaria['cta_cte_bcra'] = basem.iloc[:,27].values
monetaria['total_base'] = monetaria['billete_privado'] + monetaria['billete_publico'] + monetaria['cta_cte_bcra']
monetaria = monetaria.loc[start_date:end_date]
length = len(monetaria) # extent of how long the series you want it to be. global variable 

# Sheet Instrumentos
discardINSTRUMENTS = []

for i in range(len(instrumentos)):
    if type(instrumentos.iloc[i,0]) != type(instrumentos.iloc[8,0]):
        discardINSTRUMENTS.append(i)
    else:
        pass
interval = [max(discardINSTRUMENTS[:5]) + 1 , min(discardINSTRUMENTS[5:])]
instrumentos = instrumentos.iloc[interval[0]:interval[1]]
herramientas = pd.DataFrame(instrumentos.iloc[:,1].values,columns=['pases'],index=instrumentos.iloc[:,0].values)
herramientas['leliqs'] = instrumentos.iloc[:,4].values
herramientas['legar'] = instrumentos.iloc[:,5].values

# Sheet Reservas
discardReservas = []

for i in range(len(reservas)):
    if type(reservas.iloc[i,0]) != type(reservas.iloc[8,0]):
        discardReservas.append(i)
    else:
        pass
interval = [max(discardReservas[:8]) + 1 , min(discardReservas[8:])]
reservas = reservas.iloc[interval[0]:interval[1]]
reservorio = pd.DataFrame(reservas.iloc[:,3].values,columns=['stock_reservas'],index=reservas.iloc[:,0].values)
reservorio['tc_oficial'] = reservas.iloc[:,-1].values
indice = []
for i in range(len(reservorio.index)):
  indice.append(dt.datetime.strptime(str(reservorio.index.values[i])[0:10],'%Y-%m-%d'))
reservorio.index = indice 

# Reformat sheets into moentario main dataframe
herramientas,reservorio = herramientas.loc[start_date:end_date],reservorio.loc[start_date:end_date]
monetaria['pases'] = herramientas.pases.values
monetaria['leliqs'] = herramientas.leliqs.values
monetaria['legar'] = herramientas.legar.values
monetaria['stock_reservas'] = reservorio.stock_reservas.values

# Sheet Depositos
discardDepositos = []

for i in range(len(depositos)):
    if type(depositos.iloc[i,0]) != type(depositos.iloc[8,0]):
        discardDepositos.append(i)
    else:
        pass
    
interval = [max(discardDepositos[:6]) + 1 , min(discardDepositos[8:])]
depositos = depositos.iloc[interval[0]:]
depositos.index = range(len(depositos))

# Remove 'Prom. Month' rows
discardDepositos = []
for i in range(len(depositos)):
    if type(depositos.iloc[i,0]) != type(depositos.iloc[0,0]):
        discardDepositos.append(i)
    else:
        pass

for i in range(len(discardDepositos)):
    depositos = depositos.drop([discardDepositos[i]])

depositos.index = depositos.iloc[:,0].values    
del depositos['Gerencia de Estadísticas Monetarias']
depositos.index = [i.strftime('%Y-%m-%d') for i in depositos.index.to_list()]    
depositado = pd.DataFrame(depositos.iloc[:,1].values,columns=['cta_ctes_publico'],index=depositos.index)
depositado['cta_ctes_privado'] = depositos.iloc[:,10].values
depositado['caja_ahorro'] = depositos.iloc[:,11].values
depositado['plazos_tres'] = (depositos.iloc[:,12].values + depositos.iloc[:,13].values + depositos.iloc[:,14].values)
depositado['total_depositos_publico'] = depositos.iloc[:,11].values
depositado['total_depositos_privado'] = depositos.iloc[:,18].values
depositado['M2'] = depositos.iloc[:,-1].values
depositado = depositado.tail(length) 
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
aapl = yahoo.download("AAPL AAPL.BA",start=str(start_date)[:10],end=str(end_date)[:10])['Adj Close'].fillna(method="ffill")
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

toplot = monetaria.copy()
# Add last price in the colums so the plot appear in legend too 
toplot = toplot.rename(columns={'M3':f'M3 ${toplot["M3"].tail(1).values[0]}'})
toplot = toplot.rename(columns={'Monetary Vision':f'Monetary Vision ${toplot["Monetary Vision"].tail(1).values[0]}'})
toplot = toplot.rename(columns={'CCL AAPLBA':f'CCL AAPLBA ${toplot["CCL AAPLBA"].tail(1).values[0]}'})
toplot = toplot.rename(columns={'Fundamental Forex':f'Fundamental Forex ${toplot["Fundamental Forex"].tail(1).values[0]}'})
toplot = toplot.rename(columns={'GAP':f'GAP {toplot["GAP"].tail(1).values[0] * 100}%'})
toplot = toplot.rename(columns={'Official_Exchange_Rate':f'Official_Exchange_Rate ${toplot["Official_Exchange_Rate"].tail(1).values[0]}'})
toplot = toplot.rename(columns={'SOLIDARITY':f'SOLIDARITY ${toplot["SOLIDARITY"].tail(1).values[0]}'})

# Final plots
fig = plt.figure(figsize=(50,25))
ax1 = fig.add_subplot(111)
toplot.iloc[:,-6:-1].plot(ax=ax1, lw=10.)
ax1.set_title('Argentina Forex Spectrum', fontsize=120, fontweight='bold')
ax1.grid(linewidth=2)
ax1.legend(loc='best', bbox_to_anchor=(1., 0.85),fontsize=100)
plt.xticks(size = 80)
plt.yticks(size = 80)
plt.savefig('ArgentinaFX.png',bbox_inches='tight')

figb = plt.figure(figsize=(50,25))
ax1 = figb.add_subplot(111)
toplot.iloc[:,-1].plot(ax=ax1, lw=7.)
ax1.set_title('GAP CCL AAPLBA vs. Official', fontsize=120, fontweight='bold')
ax1.grid(linewidth=2)
ax1.legend(loc='best', bbox_to_anchor=(1., 0.85),fontsize=100)
plt.xticks(size = 80)
plt.yticks(size = 80)
plt.savefig('gap.png',bbox_inches='tight')

# save the excel
writer = pd.ExcelWriter(f'Central Bank Report {today}.xlsx',engine='xlsxwriter')
monetaria.to_excel(writer,sheet_name=f'report {today}',index=True)
writer.save()
