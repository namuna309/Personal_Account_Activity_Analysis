from django.shortcuts import render, HttpResponse
from apps.visualization.charts import Top10Chart, SlideCompBarChart, TimeLineChart, HashtagBoxPlot
from bokeh.embed import components
# Create your views here.


class ChartManager:
    def __init__(self):
        self.charts = []

    def add_chart(self, chart):
        self.charts.append(chart)

    def generate_scripts_and_divs(self):
        scripts = []
        divs = []
        for chart in self.charts:
            script, div = components(chart.run())
            scripts.append(script)
            divs.append(div)
        return scripts, divs


def combine_charts(request):
    chart_manager = ChartManager()

    chart_manager.add_chart(Top10Chart())
    chart_manager.add_chart(SlideCompBarChart())
    chart_manager.add_chart(HashtagBoxPlot())
    chart_manager.add_chart(TimeLineChart(data_type='contents'))
    chart_manager.add_chart(TimeLineChart(data_type='likes'))
    chart_manager.add_chart(TimeLineChart(data_type='comments'))

    scripts, divs = chart_manager.generate_scripts_and_divs()

    context = {
        'scripts': scripts,
        'divs': divs,
    }
    return render(request, 'web_site/combine_charts.html', context)
