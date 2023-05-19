from django.shortcuts import render, HttpResponse
from apps.visualization.charts import Top10Chart, SlideCompBarChart, TimeLineChart, HashtagBoxPlot
from bokeh.embed import components
# Create your views here.


def combine_charts(request):
    top10_chart = Top10Chart()
    pie_chart = top10_chart.run()

    slide_comp_chart = SlideCompBarChart()
    bar_chart = slide_comp_chart.run()

    time_contents_line_chart = TimeLineChart(data_type='contents')
    line_chart1 = time_contents_line_chart.run()
    time_likes_line_chart = TimeLineChart(data_type='likes')
    line_chart2 = time_likes_line_chart.run()
    time_comments_line_chart = TimeLineChart(data_type='comments')
    line_chart3 = time_comments_line_chart.run()

    hashtag_box_chart = HashtagBoxPlot()
    box_chart = hashtag_box_chart.run()

    script1, div1 = components(pie_chart)
    script2, div2 = components(bar_chart)
    script3, div3 = components(line_chart1)
    script4, div4 = components(line_chart2)
    script5, div5 = components(line_chart3)
    script6, div6 = components(box_chart)

    context = {
        'script1': script1,
        'div1': div1,
        'script2': script2,
        'div2': div2,
        'script3': script3,
        'div3': div3,
        'script4': script4,
        'div4': div4,
        'script5': script5,
        'div5': div5,
        'script6': script6,
        'div6': div6,

    }
    return render(request, 'web_site/combine_charts.html', context)
