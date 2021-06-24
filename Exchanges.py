import yfinance as yahoo
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.family'] = 'serif'
plt.style.use('fivethirtyeight')


time, duration = "1y", "60m"

stocks = ['AAPL.BA', 'BBD.BA', 'MELI.BA', 'KO.BA', 'INTC.BA', 'VALE.BA',
       'TSLA.BA', 'WFC.BA', 'XOM.BA', 'AMZN.BA', 'BABA.BA', 'T.BA', 'MSFT.BA',
       'GE.BA', 'WMT.BA', 'HMY.BA', 'PFE.BA', 'ERJ.BA', 'AUY.BA', 'X.BA']

cedears = yahoo.download(stocks, period=time, interval=duration)['Adj Close'].fillna(method='ffill')

ratios = [10,144,1,9,1,1,1,1,5,5,60,10,2,3,15,2,5,6,3,5]

cedears = cedears * ratios  # get stocks prices according to what you have to paid

topba = [s.replace('.BA', 'BA') for s in stocks]

cedears.columns = topba

forex = [i.replace('.BA','') for i in stocks]

df = yahoo.download(forex,period=time, interval=duration)['Adj Close'].fillna(method='ffill')

mervalba = ['ARS=X', 'BMA', 'BMA.BA', 'CEPU', 'CEPU.BA', 'CRES.BA', 'CRESY', 'EDN', 'EDN.BA',
            'GGAL', 'GGAL.BA', 'IRS', 'IRSA.BA', 'LOMA', 'LOMA.BA', 'PAM', 'PAMP.BA',
            'SUPV', 'SUPV.BA', 'TECO2.BA', 'TEO', 'TGS', 'TGSU2.BA', 'YPF',
            'YPFD.BA']

merval = yahoo.download(tickers=mervalba, period=time, interval=duration)['Adj Close'].fillna(method='ffill')

top = list(merval.columns)
topmerval = [t.replace('.BA', 'BA') for t in top]

merval.columns = topmerval

cable = pd.DataFrame(data=None)

cable['BMA'] = (merval.BMABA / merval.BMA) * 10
cable['CEPU'] = (merval.CEPUBA / merval.CEPU) * 10
cable['CRES'] = (merval.CRESBA / merval.CRESY) * 10
cable['EDN'] = (merval.EDNBA / merval.EDN) * 20
cable['GGAL'] = (merval.GGALBA / merval.GGAL) * 10
cable['IRSA'] = (merval.IRSABA / merval.IRS) * 10
cable['LOMA'] = (merval.LOMABA / merval.LOMA) * 5
cable['PAMP'] = (merval.PAMPBA / merval.PAM) * 25
cable['SUPV'] = (merval.SUPVBA / merval.SUPV) * 5
cable['TECO2'] = (merval.TECO2BA / merval.TEO) * 5
cable['TGSU2'] = (merval.TGSU2BA / merval.TGS) * 5
cable['YPF'] = (merval.YPFDBA / merval.YPF)

mediacable = pd.DataFrame(index=cable.index)
mediacable['CableAdrs'] = cable.T.median()

df = df.tail(len(cedears))

tc = cedears.div(df.values)
tc.columns = topba

mediaced = pd.DataFrame(index=tc.index)
mediaced['CableCedears'] = tc.T.median()

dolar = pd.DataFrame(index=merval.index)
dolar['solidario+30+35'] = merval.iloc[:, 0] * 1.30 * 1.35

fig = plt.figure(figsize=(50, 25))
ax1 = fig.add_subplot(111)
mediaced.fillna(method='ffill').plot(ax=ax1, color='g', lw=7., legend=True)
mediacable.fillna(method='ffill').plot(ax=ax1, color='b', lw=7., legend=True)
dolar.plot(ax=ax1, color='r', lw=14., legend=True)
ax1.set_title('Exchange Rates Argentina',fontsize=120,fontweight='bold')
ax1.grid(True,color='k',linestyle='-.',linewidth=2)
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=80)
plt.xticks(size = 60)
plt.yticks(size = 60)
plt.savefig('Exchanges.png',bbox_inches='tight')
plt.show()
