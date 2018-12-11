from bokeh.models import ColumnDataSource, HoverTool, Paragraph
from bokeh.plotting import figure
from bokeh.palettes import all_palettes
from bokeh.layouts import column

from modules.base import BaseModule
from utils import run_query
from states import NAMES_TO_CODES


QUERY = """
SELECT 
      primer,
      SUM(num_reads) AS num_reads
      FROM ((SELECT sample_id 
             FROM `clearlabs-science.qaptrdb.blastrecords` 
             GROUP BY sample_id) as B
      JOIN `clearlabs-science.qaptrdb.primer2alleles` as P
      ON B.sample_id=P.sample_id
      AND B.sample_id='%(sample_id)s')
      GROUP BY primer

"""

TITLE = 'Number of reads per primer:'


class Module(BaseModule):

    def __init__(self):
        super().__init__()
        self.source = None
        self.plot = None
        self.title = None

    def fetch_data(self, sample_id):
      # Remove after tested
      sample_id = "CL104"
      my_df = pandas.io.gbq.read_gbq(
         query,
         project_id='clearlabs-science',
         private_key=PRIVATE_KEY,
         dialect='standard',
         reauth=True
      )
      return my_df
#       return run_query(
#           QUERY % {'sample_id': sample_id},
#           cache_key=('colab-%s' % sample_id))

# [START make_plot]
    def make_plot(self, dataframe):
        self.source = ColumnDataSource(data=dataframe)
        hover_tool = HoverTool(tooltips=[
            ("Numer of reads", "$num_reads"),
            ("Primer", "@primer"),
        ])
        
        
        self.plot = figure(
            plot_width=600, plot_height=300, tools=[hover_tool],
            toolbar_location=None)
        columns = {
            'primer': 'Number of reads for primer',
        }
        self.plot.line(
            x='year', y='primer', source=self.source, line_width=3,
            line_alpha=0.6)

        self.title = Paragraph(text=TITLE)
        return column(self.title, self.plot)
# [END make_plot]

    def update_plot(self, dataframe):
        self.source.data.update(dataframe)

    def busy(self):
        self.title.text = 'Updating...'
        self.plot.background_fill_color = "#efefef"

    def unbusy(self):
        self.title.text = TITLE
        self.plot.background_fill_color = "white"
