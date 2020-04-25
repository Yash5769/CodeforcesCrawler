from . import scrape
from .models import languages,verdicts,level
from collections import OrderedDict
from . import fusioncharts

def get_submission_chart(handle):
    scrape.get_submission(handle)
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Languages of "+handle
    chartConfig["xAxisName"] = "Language"
    chartConfig["yAxisName"] = "Submissions"
    chartConfig["theme"] = "fusion"
    chartConfig["animation"] = "1"
    datasource = OrderedDict()
    datasource["Chart"] = chartConfig
    datasource["data"] = []
    for l in languages.objects.all():
        datasource["data"].append({"label": l.name, "value": str(l.val)})
    column2D = fusioncharts.FusionCharts("pie2d", "myFirstChart", "600", "400", "chart1", "json", datasource)
    return column2D

def get_verdict_chart(handle):
    # scrape.get_submission(handle)
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Verdict of "+handle
    chartConfig["xAxisName"] = "Verdicts"
    chartConfig["yAxisName"] = "Submissions"
    chartConfig["theme"] = "fusion"
    chartConfig["animation"] = "1"
    datasource = OrderedDict()
    datasource["Chart"] = chartConfig
    datasource["data"] = []
    WA = 0
    CE = 0
    TLE = 0
    AC = 0
    SK = 0
    MLE =0
    for l in verdicts.objects.all():
        datasource["data"].append({"label": l.name, "value": l.val})
    column2D = fusioncharts.FusionCharts("pie2d", "see", "600", "400", "chart2", "json", datasource)
    return column2D

def get_level_chart(handle):
    # scrape.get_submission(handle)
    chartConfig = OrderedDict()
    chartConfig["caption"] = "level of "+handle
    chartConfig["xAxisName"] = "Levels"
    chartConfig["yAxisName"] = "Submissions"
    chartConfig["theme"] = "fusion"
    chartConfig["animation"] = "1"
    datasource = OrderedDict()
    datasource["Chart"] = chartConfig
    datasource["data"] = []
    for l in level.objects.all():
        datasource["data"].append({"label": l.name, "value": l.val})
    column2D = fusioncharts.FusionCharts("column2d", "seed", "600", "400", "chart3", "json", datasource)
    return column2D
