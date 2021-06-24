style = '''\
<!DOCTYPE html>
<html>
<head>
<style>
body {
  font-family: 'Trebuchet MS', sans-serif;
}

.header {
  padding: 30px;
  text-align: center;
  background: rgb(0,0,0);
  color: white;
  font-size: 30px;
}

tr:hover {background-color:rgb(150,150,150); color:white;}

/* Create two equal columns that sits next to each other */

table, th, td, tr {
  font-size: 10px;
  border: 1px solid black;
  padding: 5px;
  border-collapse: collapse;
  text-align: center;   
  width: 1%;
  white-space: nowrap;
  margin-left: auto; 
  margin-right: auto;
}
th {
  color: white;
}
table {
  border-spacing: 5px;
  width: 20%;
}
</style>
</head>
<body>
'''
end_html =''' 
</body>
</html>'''


highlight = """<div class="header">
                <h1>Argentina Forex Report</h1>
              </div> """

explanation = """\
        <h3>The current scenario in Argentina offers us 5 differents metrics in order to diagnose the stability of argentinian currency Peso.<br />Which are:\
          <ul>
                <li>Official Rate: given by the goverment.</li>
                <li>Official Solidarity Rate: it is a reference of the Official Rate plus taxes of 65%.</li>
                <li>Fundamental Forex: provided by dividing the liabilities of the Central Bank (BCRA) by the reserves.</li>
                <li>CCL AAPL.BA: convertion as a result of Apple US Stock divided by argentinian ADR (most representative as it holds 15% of Cedears volume).</li>
                <li>Monetary Vision: Official Rate plus the difference between the return of CCL AAPL.BA and the increase of Monetary Base.<br />As if Monetary Base and the Official Rate are perfectly correlated</li>
          </ul><br /></h3>"""

curve_futures = """<h3>Dollar Futures Curve Rofex.</h3><br /><h5>Time series and return from the current futures contracts available.</h5>"""


endWords = """<h3>Lessons and opportunities to keep an eye on:</h3>
             <h5><ul>
                <li>Eliminate uncertainty and risk.</li>
                <li>Forex Carry trade: going long in the spot and short on futures.</li>
                <li>Compare Solidarity Exchange Rate versus Apple Cedear for signals.</li>
              </ul></h5><br />
              <h2>KEEP UPDATED OF THE MARKET</h2>"""  
