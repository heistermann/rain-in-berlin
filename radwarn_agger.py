
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
#
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # Zonal Statistics Example

# In[58]:

import wradlib as wrl
import matplotlib.pyplot as pl
import matplotlib as mpl
import warnings
warnings.filterwarnings('ignore')
#try:
#    get_ipython().magic("matplotlib inline")
#except:
#    pl.ion()
import numpy as np
import os

from numpy.lib.stride_tricks import as_strided as ast
import json
from collections import OrderedDict, defaultdict

import pandas as pd
import colorcet as cc


# In[56]:

import bokeh
from bokeh.layouts import row, column
from bokeh.io import show, output_file, save
from bokeh.plotting import figure
from bokeh import events
from bokeh.models import (
    ColumnDataSource,
    Panel,
    Legend,
    CrosshairTool,
    Tabs,
    HoverTool,
    TapTool,
    ResetTool,
    WheelZoomTool,
    CustomJS,
    ColorBar,
    LinearColorMapper,
    FixedTicker,
    LogTicker,
    GeoJSONDataSource,
    DatetimeTicker,
    DatetimeTickFormatter
)


# In[2]:

#get_ipython().magic('pylab')


# ## Setup Examples

# In[3]:

def norm_shape(shape):
    '''
    Normalize numpy array shapes so they're always expressed as a tuple,
    even for one-dimensional shapes.

    Parameters
        shape - an int, or a tuple of ints

    Returns
        a shape tuple
    '''
    try:
        i = int(shape)
        return (i,)
    except TypeError:
        # shape was not a number
        pass

    try:
        t = tuple(shape)
        return t
    except TypeError:
        # shape was not iterable
        pass

    raise TypeError('shape must be an int, or a tuple of ints')


def sliding_window(a, ws, ss=None, flatten=True):
    # taken from http://www.johnvinyard.com/blog/?p=268
    """
    Return a sliding window over a in any number of dimensions

    Parameters:
        a  - an n-dimensional numpy array
        ws - an int (a is 1D) or tuple (a is 2D or greater) representing the size
             of each dimension of the window
        ss - an int (a is 1D) or tuple (a is 2D or greater) representing the
             amount to slide the window in each dimension. If not specified, it
             defaults to ws.
        flatten - if True, all slices are flattened, otherwise, there is an
                  extra dimension for each dimension of the input.

    Returns
        an array containing each n-dimensional window from a
    """

    if None is ss:
        # ss was not provided. the windows will not overlap in any direction.
        ss = ws
    ws = norm_shape(ws)
    ss = norm_shape(ss)

    # convert ws, ss, and a.shape to numpy arrays so that we can do math in every
    # dimension at once.
    ws = np.array(ws)
    ss = np.array(ss)
    shape = np.array(a.shape)

    # ensure that ws, ss, and a.shape all have the same number of dimensions
    ls = [len(shape), len(ws), len(ss)]
    if 1 != len(set(ls)):
        raise ValueError(
            'a.shape, ws and ss must all have the same length. They were %s' % str(
                ls))

    # ensure that ws is smaller than a in every dimension
    if np.any(ws > shape):
        raise ValueError(
            'ws cannot be larger than a in any dimension.      a.shape was %s and ws was %s' % (
            str(a.shape), str(ws)))

    # how many slices will there be in each dimension?
    newshape = norm_shape(((shape - ws) // ss) + 1)
    # the shape of the strided array will be the number of slices in each dimension
    # plus the shape of the window (tuple addition)
    newshape += norm_shape(ws)
    # the strides tuple will be the array's strides multiplied by step size, plus
    # the array's strides (tuple addition)
    newstrides = norm_shape(np.array(a.strides) * ss) + a.strides
    strided = ast(a, shape=newshape, strides=newstrides)
    if not flatten:
        return strided

    # Collapse strided so that it has one more dimension than the window.  I.e.,
    # the new array is a flat list of slices.
    meat = len(ws) if ws.shape else 0
    firstdim = (np.product(newshape[:-meat]),) if ws.shape else ()
    dim = firstdim + (newshape[-meat:])
    # remove any dimensions with size 1
    dim = filter(lambda i: i != 1, dim)
    return strided.reshape(list(dim))


# ## Zonal Stats Rectangular Grid

# In[4]:

from matplotlib.collections import PatchCollection
from matplotlib.colors import from_levels_and_colors
import matplotlib.patches as patches
import datetime as dt
from osgeo import osr


# In[5]:

# check for GEOS enabled GDAL
if not wrl.util.has_geos():
    print("NO GEOS support within GDAL, aborting...")
    exit(0)


output_file("agger.html", title='Radwarn Agger Catchment')
starttime = dt.datetime.now()

# ### Create Projections

# In[6]:

# create radolan projection osr object
proj_stereo = wrl.georef.create_osr("dwd-radolan")

# create Gauss Krueger zone 2 projection osr object
proj_gk = osr.SpatialReference()
proj_gk.ImportFromEPSG(31466)


# ### Get River Catchments

# In[7]:

# Open shapefile (already in GK2)
shpfile = 'shapefiles/agger/agger_merge.shp'
dataset, inLayer = wrl.io.open_shape(shpfile)
cats, keys = wrl.georef.get_shape_coordinates(inLayer)
print(len(cats))


# ### Read netcdf Composite data file

# In[8]:

composite_path = '/data/malted/radmon_rt/composite/MONITOR/'
radmon_path = '/data/malted/radmon_rt/composite/MONITOR/'
import glob
import datetime as dt
today = dt.datetime.now()
day = dt.timedelta(days=1)
yesterday = today-day
files = []
md1 = '{0}{1:02}{2:02}'.format(today.year,today.month, today.day)
md2 = '{0}{1:02}{2:02}'.format(yesterday.year,yesterday.month, yesterday.day)
print(md1, md2)
print(radmon_path)
pth1 = os.path.join(radmon_path, '{0}/*hkm-bonjue-2d-MONITOR+rx.nc'.format(md1))
pth2 = os.path.join(radmon_path, '{0}/*hkm-bonjue-2d-MONITOR+rx.nc'.format(md2))
print(pth1)
files.extend(glob.iglob(pth1))
files.extend(glob.iglob(pth2))
files = sorted(files)[-144:]
cdata = wrl.io.read_generic_netcdf(files[0])

# # In[9]:
#
cvars = cdata['variables']
x = cvars['x']
y = cvars['y']
X = x['data']
Y = y['data']
XY = np.dstack(np.meshgrid(X, Y))
# rr = cvars['xband_oase_rr']
# RR = rr['data']
# # transform radolan polar stereographic projection to GK2
xy = wrl.georef.reproject(XY,
                          projection_source=proj_stereo,
                          projection_target=proj_gk)
# data = RR.copy()
# data[data>=300] = 0.
#
#
# # ### Diagnostic Plot
#
# # In[10]:
#
# print(XY.shape, RR.shape, data[0,0])
#
# print(np.nanmax(RR))
# fig = pl.figure(figsize=(10,8))
# ax = fig.add_subplot(111, aspect="equal")
# ax.pcolormesh(XY[..., 0], XY[..., 1], np.ma.masked_equal(data, 0), vmin=0, vmax=np.nanmax(data))


# do this only once
# In[11]:

# Reduce grid size using a bounding box (to enhancing performance)
bbox = inLayer.GetExtent()
buffer = 5000.
bbox = dict(left=bbox[0] - buffer, right=bbox[1] + buffer,
            bottom=bbox[2] - buffer, top=bbox[3] + buffer)
mask, shape = wrl.zonalstats.mask_from_bbox(xy[..., 0], xy[..., 1],
                                                bbox)
#xy_ = np.vstack((xy[..., 0][mask].ravel(), xy[..., 1][mask].ravel())).T
#data_ = data[mask]


# In[12]:

#print(data_.shape, data.ravel().shape)


# In[13]:

###########################################################################
# Approach #1: Assign grid points to each polygon and compute the average.
#
# - Uses matplotlib.path.Path
# - Each point is weighted equally (assumption: polygon >> grid cell)
# - this is quick, but theoretically dirty
###########################################################################

t1 = dt.datetime.now()

# # Create instance of type ZonalDataPoint from source grid and
# # catchment array
# zd = wrl.zonalstats.ZonalDataPoint(xy_, cats, srs=proj_gk, buf=500.)
# # dump to file (for later use - see below)
# zd.dump_vector('test_zonal_points_cart')
# # Create instance of type GridPointsToPoly from zonal data object
# obj1 = wrl.zonalstats.GridPointsToPoly(zd)
#
# isecs1 = obj1.zdata.isecs  # for plotting (see below)

t2a = dt.datetime.now()
print("Approach #1 computation time:")
print("\tCreate object from scratch: %f "
      "seconds" % (t2a - t1).total_seconds())
# Create instance of type GridPointsToPoly from zonal data file
# (much faster)
obj1 = wrl.zonalstats.GridPointsToPoly('test_zonal_points_cart')

# In[14]:

t2b = dt.datetime.now()
# Compute stats for target polygons
#avg1 = obj1.mean(data_.ravel())
#var1 = obj1.var(data_.ravel())

t3 = dt.datetime.now()

# Create instance of type GridPointsToPoly from zonal data file
# (much faster)
#obj1 = wrl.zonalstats.GridPointsToPoly('test_zonal_points_cart')

t4 = dt.datetime.now()

print("Approach #1 computation time:")
print("\tCreate object from scratch: %f "
      "seconds" % (t2a - t1).total_seconds())
print("\tCreate object from dumped file: %f "
      "seconds" % (t4 - t3).total_seconds())
print("\tCompute stats using object: %f "
      "seconds" % (t3 - t2b).total_seconds())

# PLOTTING Approach #1

# # Just a test for plotting results with zero buffer
# zd2 = wrl.zonalstats.ZonalDataPoint(xy_, cats, buf=0)
# # Create instance of type GridPointsToPoly from zonal data object
# obj2 = wrl.zonalstats.GridPointsToPoly(zd2)
# isecs2 = obj2.zdata.isecs


# In[15]:




# In[30]:

avg = []
var = []
dt_src = []
for i, cfile in enumerate(files):
    #print(i, cfile)
    cdata = wrl.io.read_generic_netcdf(cfile)
    cvars = cdata['variables']
    dt_src.append(dt.datetime.fromtimestamp(cvars['time']['data']))
    rr = cvars['xband_oase_rr']
    RR = rr['data']
    data = RR.copy()
    data[data>=300] = 0.
    data_ = data[mask]
    avg.append(obj1.mean(data_.ravel()))
    var.append(obj1.var(data_.ravel()))



# In[66]:

avg1 = np.vstack(avg)
var1 = np.vstack(var)
print(avg1.shape, var1.shape)
#print(dt_src)


# ### Bokeh Generation and Plotting

# In[37]:

s = []
rain = avg1.T
rain[rain < 0.01] = 0.
s.append(rain)
cph = 12
total = rain.shape[1]
n_catch = rain.shape[0]
for hours in range(1, 7, 1):
    sw = sliding_window(rain, (1, cph * hours), (1, 1))
    print(sw.shape)
    sw.shape = (n_catch, total - cph * hours + 1, cph * hours)
    sx = np.sum(sw, -1)
    sx = np.concatenate((np.zeros((n_catch, cph * hours - 1)), sx), axis=1)
    s.append(sx)


# In[69]:

idx = 6*12
dt_src1 = dt_src[-idx:]
rain = np.squeeze(s)[..., -idx:]
print("Rain.shape", rain.shape)
print(rain.flatten().reshape(72,-1).shape)
print(dt_src1[0], dt_src1[-1])
last = dt_src1[-1]

# In[71]:

with open(r'agger_merge.geojson', 'r') as f:
    agger_dict = json.loads(f.read(), object_hook=OrderedDict)


# In[72]:

# create DataFrame
df=[]
print("RAIN:", rain.shape)
dates = pd.date_range(dt_src1[0].strftime("%Y%m%d%H%M%S"), periods=72, freq="300s")
for i in range(rain.shape[1]):
    #print(i)
    r = rain[:, i, :].T.copy()
    idf = pd.DataFrame(r.reshape(-1, 7), index=dates, columns=['0hour', '1hour', '2hour', '3hour', '4hour', '5hour', '6hour'])
    cat = agger_dict['features'][i]['properties']['name']
    #print(cat)
    idf.insert(0, 'catch', cat)
    df.append(idf)
dfm = pd.concat(df)
#from IPython.display import display
#display(dfm.head())


# In[82]:

rain1 = np.squeeze(rain[0,:,-1])

for i, v in enumerate(agger_dict['features']):
    v['properties']['id'] = i
    v['properties']['rainrate'] = rain1[i]

#for k, v in agger_dict['features'][10].items():
    #print(k, v)


# In[83]:

# create DataSource
agger = GeoJSONDataSource(geojson=json.dumps(agger_dict))


# In[75]:

# color handling
palette = cc.b_rainbow_bgyr_35_85_c72
#color_mapper = LinearColorMapper(palette=palette, low=0, high=150)
linpalette = bokeh.palettes.linear_palette(palette, 20)
color_mapper = LinearColorMapper(palette=linpalette, low=0, high=100)
colorlist = bokeh.palettes.linear_palette(palette, 13)
sumcolors = bokeh.palettes.linear_palette(palette, 7)
#print(colorlist)

#id = [ft['properties']['id'] for ft in agger_dict['features']]
name = [ft['properties']['name'] for ft in agger_dict['features']]
#######print(name)


# In[76]:

source1 = ColumnDataSource(dfm.loc[dfm.index[-1]])


# In[77]:

#source2 = []
#for ct in name:
#    #print(ct)
#    linedict = defaultdict(list)
#    for i, v in enumerate(['1hour', '2hour', '3hour', '4hour', '5hour', '6hour']):
#        linedict['index'].append(dfm[dfm['catch'] == ct].index)
#        linedict['rain'].append(dfm[dfm['catch'] == ct][v])
#        linedict['tag'].append(v)
#        linedict['color'].append(sumcolors[i])
#    source2.append(ColumnDataSource(linedict))


# In[78]:

lp_source = []
#for ct in name:
for i, v in enumerate(['0hour', '1hour', '2hour', '3hour', '4hour', '5hour', '6hour']):
    #print(i,v)
    linedict = defaultdict(list)
    for k, ct in enumerate(name):
        linedict['index'].append(dfm[dfm['catch'] == ct].index)
        linedict['rain'].append(dfm[dfm['catch'] == ct][v])
        linedict['sum'].append(v)
        linedict['tag'].append(ct)
        linedict['color'].append(colorlist[k])
    lp_source.append(ColumnDataSource(linedict))


# In[84]:

# Tools options
hover_opts_lineplot = dict(
    tooltips=[("Catchment", "@tag"), ("index", "$x{int}"), ("Rainsum", '$y')],
    show_arrow=True,
    line_policy='next',
    mode='mouse',
)

hover_opts_shapeplot = dict(
    tooltips=[("Catchment", "@name"), ("Area", "@AREA"), ("Rainsum", "@rainrate"),
              ("Lon, Lat", "$x, $y")],
    show_arrow=False,
    line_policy='next'
)

hover_opts_barplot = dict(
    tooltips=[("Catchment", "@catch"), ("Rain", "@0hour")],
    # tooltips="""
    #     <HEAD>
    #     <style>
    #     .bk-tooltip {
    #         background-color: transparent !important;
    #         border: transparent !important;
    #         border-top-color: transparent !important;
    #         border-bottom-color: transparent !important;
    #         border-left-color: transparent !important;
    #         border-right-color: transparent !important;
    #         }
    #     </style>
    #     </HEAD>
    #     <HTML>
    #     <div>
    #         <span style="font-size: 20px; font-weight:bold;">@catch</span>
    #         </br>
    #         <span style="font-size: 20px; font-weight:bold;">@1hour mm</span>
    #     </div>
    #     </HTML>
    #     """,
    show_arrow=False,
    line_policy='next'
)

cb_tapping = CustomJS(args={'agger':agger, 'source1': source1,
                            'lp0': lp_source[0],
                            'lp1': lp_source[1],
                            'lp2': lp_source[2],
                            'lp3': lp_source[3],
                            'lp4': lp_source[4],
                            'lp5': lp_source[5],
                            'lp6': lp_source[6],

                            },
    code="""
        var f = cb_obj.selected
        sel1d1 = f
        console.log("Tapped", cb_obj)
        agger.selected = sel1d1
        source1.selected = sel1d1
        lp0.selected = sel1d1;
        lp1.selected = sel1d1;
        lp2.selected = sel1d1;
        lp3.selected = sel1d1;
        lp4.selected = sel1d1;
        lp5.selected = sel1d1;
        lp6.selected = sel1d1;
    """)


def create_shapeplot(src, tools):
    shape = figure(height=400, width=700,
                   title="Current Rainrate [mm/h] - {}".format(dt_src1[-1]),
                   tools=tools, toolbar_location="above",
                   x_axis_location=None, y_axis_location=None)
    shape.grid.grid_line_color = None
    ptc = shape.patches('xs', 'ys', source=src,
                  fill_color={'field': 'rainrate', 'transform': color_mapper},
                  fill_alpha=0.85, line_color="white", line_width=0.5,
                  nonselection_fill_alpha=0.5,
                  nonselection_line_color="grey",
                  nonselection_fill_color={'field': 'rainrate',
                                           'transform': color_mapper},
                  hover_alpha=1.0, hover_line_color="black",
                  hover_fill_color={'field': 'rainrate',
                                    'transform': color_mapper})

    return shape, ptc

ht1 = HoverTool(**hover_opts_shapeplot, callback=CustomJS(args={'source': source1},
    code="""
        var f = cb_obj.value
        //console.log("Tapped", f)
        //console.log(cb_obj)
        //console.log(cb_data)
    """))

tt1 = TapTool(callback=cb_tapping)

shape, ptc = create_shapeplot(agger, [ht1, tt1, ResetTool()])


def create_barplot(src, tools):
    rectplot = figure(height=400, width=700,
                      title="Akkumulierte Regensumme [mm]",
                      tools=tools, toolbar_location='above',
                      x_range=name)
    rectplot.xaxis.major_label_orientation = np.pi / 2
    vbar = rectplot.vbar(x='catch', bottom=0, top='0hour', width=0.5,
                         source=src)#, fill_color={'field': 'rain', 'transform': color_mapper},)
    return rectplot, vbar


ht2 = HoverTool(**hover_opts_barplot)

tt2 = TapTool(callback=cb_tapping)

rectplot, vbar = create_barplot(source1, [ht2, tt2, ResetTool()])


#id = [ft['properties']['id'] for ft in agger_dict['features']]
name = [ft['properties']['name'] for ft in agger_dict['features']]
rainrate = [ft['properties']['rainrate'] for ft in agger_dict['features']]


# In[85]:

cb_tab = CustomJS(args={'vbar': vbar, 'ht': ht2, 'source': source1},
    code="""
        var f = cb_obj.changed.active + 1
        vbar.attributes.glyph.attributes.top.field = f + 'hour'
        ht.attributes.tooltips[1][1] = '@' + f + 'hour'
        source.trigger('change');
    """)



def create_lineplot(src, callback, **ht_opts):
    lineplot = []
    for item in src:
        sum = item.to_df()['sum'][0]
        lp = figure(height=400, width=700,
                    toolbar_location='right',
                    title="Akkumulierte Regensumme [mm]",
                    tools=[HoverTool(**ht_opts),
                           TapTool(callback=cb_tapping),
                           CrosshairTool(dimensions='height'),
                           ResetTool()])
        #cl = lp.circle(x='index', y='rain', source=item)
        ml = lp.multi_line(xs='index', ys='rain', source=item,
                           #line_color='color',
                           line_color='blue',
                           line_alpha=0.7,
                           line_width=2,
                           hover_line_color='black', hover_line_alpha=1.0)
        lp.xaxis.major_label_orientation = np.pi/4
        lp.xaxis.axis_label = 'UTC Time'
        lp.xaxis[0].ticker = DatetimeTicker()
        lp.xaxis[0].formatter = DatetimeTickFormatter(years='%Y',
                                                   months='%Y-%m',
                                                   days='%Y-%m-%d',
                                                   hours='%H:%M',
                                                   hourmin='%H:%M',
                                                   minutes='%H:%M',
                                                   )
        lp.xaxis[0].ticker.desired_num_ticks = 30
        lp.xaxis[0].ticker.num_minor_ticks = 15
        lineplot.append(Panel(child=lp, title=sum))

    return Tabs(tabs=lineplot, callback=callback)

cticker = FixedTicker(ticks=[i for i in range(0, 101, 5)])
color_bar = ColorBar(color_mapper=color_mapper, ticker=cticker, major_tick_line_color='black',
                     label_standoff=6, border_line_color=None, location=(0,0))

shape.add_layout(color_bar, 'right')


lineplot = create_lineplot(lp_source, cb_tab, **hover_opts_lineplot)


first_row = row(shape, responsive=True)
second_row = row(rectplot, responsive=True)
third_row = row(lineplot, responsive=True)
main_column = column(first_row, second_row, third_row, responsive=True)
layout = column(main_column, responsive=True)

output_file("agger.html", title='Radwarn Agger-Catchment')
stoptime = dt.datetime.now()
print("Approach #1 computation time:")
print("\tCreate radwarn agger from scratch: %f "
      "seconds" % (stoptime - starttime).total_seconds())
save(layout)
