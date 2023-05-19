from math import pi
import pandas as pd
import seaborn as sns
from bokeh.palettes import Category20c
from bokeh.models import OpenURL, TapTool, ColumnDataSource, Whisker
from bokeh.palettes import Spectral6
from bokeh.plotting import figure, output_file
from bokeh.transform import cumsum
from apps.explore_tab_crawling.models import Hashtag, Content


class Top10Chart:
    def __init__(self):
        self.hashtag_dict = {}
        self.top10 = None

    def _count_hashtags(self):
        hashtags = Hashtag.objects.all().only('text')

        for hashtag in hashtags:
            text = hashtag.text

            if text not in self.hashtag_dict:
                self.hashtag_dict[text] = 1
            else:
                self.hashtag_dict[text] += 1

        self.hashtag_dict = sorted(self.hashtag_dict.items(),
                                   key=lambda x: x[1], reverse=True)

        self.top10 = self.hashtag_dict[:10]

    def _create_chart(self):
        self.top10 = dict((x[1:], y) for x, y in self.top10)

        output_file("openurl.html")

        data = pd.Series(self.top10).reset_index(
            name='value').rename(columns={'index': 'hashtag'})

        data['angle'] = data['value'] / data['value'].sum() * 2 * pi
        data['color'] = Category20c[len(self.top10)]

        p = figure(height=350, title="Pie Chart", toolbar_location=None,
                   tools="tap", tooltips="@hashtag: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='hashtag', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        url = "https://www.instagram.com/explore/tags/@hashtag"
        clicktool = p.select(type=TapTool)
        clicktool.callback = OpenURL(url=url)

        return p

    def run(self):
        self._count_hashtags()
        chart = self._create_chart()
        return chart


class SlideCompBarChart:
    def __init__(self):
        self.slide_tf = ['False', 'True']
        self.count_tf = [0, 0]

    def _count_slide_tf(self):
        slide_tf_posts = Content.objects.all().only('slide')

        for slide_tf_post in slide_tf_posts:
            if slide_tf_post.slide == True:
                self.count_tf[1] += 1
            else:
                self.count_tf[0] += 1

    def _create_chart(self):
        p = figure(x_range=self.slide_tf, height=350,
                   title="슬라이드 유무에 따른 콘텐츠 수", toolbar_location=None, tools="")

        if self.count_tf[0] > self.count_tf[1]:
            color_list = [Spectral6[5], Spectral6[0]]
        else:
            color_list = [Spectral6[0], Spectral6[5]]

        p.vbar(x=self.slide_tf, top=self.count_tf,
               width=0.5, color=color_list)

        p.xgrid.grid_line_color = None
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.y_range.start = 0

        return p

    def run(self):
        self._count_slide_tf()
        chart = self._create_chart()
        return chart


class TimeLineChart:
    def __init__(self, data_type):
        self.time_list = [i for i in range(24)]
        self.count_data = [0 for i in range(24)]
        self.data_type = data_type

    def _count_every_hour(self):
        contents = Content.objects.all()

        for content in contents:
            created_hour = int(content.created_at.strftime("%H"))
            if self.data_type == 'contents':
                self.count_data[created_hour] += 1
            elif self.data_type == 'likes':
                self.count_data[created_hour] += content.likes
            elif self.data_type == 'comments':
                self.count_data[created_hour] += content.comments

    def _create_chart(self):
        data = {
            'Time': self.time_list,
            'Data': self.count_data
        }

        df = pd.DataFrame(data)
        source = ColumnDataSource(df)

        p = figure(title=f'시간대별 {self.data_type} 개수',
                   x_axis_label='시간', y_axis_label='개수', height=350)

        if self.data_type == 'comments':
            color = Spectral6[1]
        elif self.data_type == 'likes':
            color = Spectral6[3]
        else:
            color = Spectral6[5]

        p.line(x='Time', y='Data', line_color=color, line_width=3,
               legend_label=self.data_type, source=source)

        return p

    def run(self):
        self._count_every_hour()
        chart = self._create_chart()
        return chart


class HashtagBoxPlot:
    def __init__(self):
        self.hashtag_count = [0 for _ in range(len(Content.objects.all()))]

    def _count_hashtag(self):
        hashtags = Hashtag.objects.all()

        for hashtag in hashtags:
            hashtag_index = hashtag.content_id.content_id
            self.hashtag_count[hashtag_index - 1] += 1

    def _create_chart(self):
        series = pd.Series(self.hashtag_count)

        qmin, q1, q2, q3, qmax = series.quantile([0, 0.25, 0.5, 0.75, 1])
        iqr = q3 - q1
        upper = q3 + 1.5 * iqr
        lower = q1 - 1.5 * iqr
        mean = series.mean()

        out = series[(series > upper) | (series < lower)]

        if not out.empty:
            outlier = list(out.values)

        k = 'hashtag'
        p = figure(tools='save', x_range=[
                   k], title="Boxplot", width=250, height=350)

        upper = min(qmax, upper)
        lower = max(qmin, lower)

        hbar_height = (qmax - qmin) / 350

        # stems
        p.segment([k], lower, [k], q1, line_color="black")
        p.segment([k], upper, [k], q3, line_color="black")

        # boxes
        p.vbar([k], 0.7, q2, q3, line_color="black")
        p.vbar([k], 0.7, q1, q2, line_color="black")

        # whiskers (almost-0 height rects simpler than segments)
        p.rect([k], lower, 0.2, hbar_height, line_color="black")
        p.rect([k], upper, 0.2, hbar_height, line_color="black")

        if not out.empty:
            p.circle([k] * len(outlier), outlier, size=6, fill_alpha=0.6)

        return p

    def run(self):
        self._count_hashtag()
        chart = self._create_chart()
        return chart
