import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('medical_examination.csv')
df.head()

# add 'overweight' Column
df['overweight'] = df['weight']/((df['height']/100)**2)
df

df.loc[df['overweight'] > 25, 'overweight'] = 1
df.loc[df['overweight'] != 1, 'overweight'] = 0

# normalising data
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] >= 1, 'gluc'] = 1

# draw Categorical Plot
def draw_cat_plot():

  # create df for cat plot using `pd.melt` using just values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars = ["cardio"], value_vars =['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # group & reformat data to split by 'cardio'. Show counts of each feature. Have to rename one of the columns for the catplot to work correctly.
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio','variable','value'], as_index = False).count()

    # draw catplot with 'sns.catplot()'
    fig = sns.catplot(x="variable", y="total", hue="value", col="cardio",data=df_cat, kind="bar")

    # save fig
    fig.savefig('catplot.png')
    return fig

# draw Heat Map
def draw_heat_map():
    # clean data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi'])&
                 (df['height'] >= df['height'].quantile(0.025))&
                 (df['height'] <= df['height'].quantile(0.975))&
                 (df['weight'] >= df['weight'].quantile(0.025))&
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # calculate correlation matrix
    corr = df_heat.corr()

    # generate mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # set up matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # draw heatmap with 'sns.heatmap()'
    sns.heatmap(corr, 
            mask=mask, 
            vmin=-0.16, 
            vmax=0.3, 
            center=0, 
            annot=True, 
            fmt=".1f", 
            cbar_kws={"shrink": 0.5, 'ticks': [-0.08, 0.00, 0.08, 0.16, 0.24]})

    # save fig
    fig.savefig('heatmap.png')
    return fig

draw_cat_plot()

draw_heat_map()
