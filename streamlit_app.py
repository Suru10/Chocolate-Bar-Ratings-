#importing general objects
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
import plotly.figure_factory as ff

#INTRODUCTIONS
st.subheader('Machine Masters')
st.write('Hi my name is Sammi, I am a senior, and I have experience with python, tableau, looker studio, pandas, plotly, and SQL, and have been programming with multiple languages in the past 4 years.')
st.write('Hey my name is Anya, I am a junior, and I have been programming since a young age. I started with Scratch and then broadened my knowledge through languages such as HTML, Swift, Java, and now Python. I have running projects in Swift and Java such as Connect 4, Wordle, Blackjack, and more! I am also super interested in AI and ML, taking courses on Coursera and reading in my spare time to learn more!')
st.write('Hi my name is Jack, I am a junior, and I have five years of coding experience in languages such as javascript, html, java, and python')
st.write('Hi my name is Elijah, I am a senior in high school, and for the past five months, I have been coding with python after starting from Scratch.')

#TITLE
st.title('Chocolate Bar Ratings EDA')
st.write('The chocolate rating dataset was scraped from flavours of cacao. The dataset comprises various chocolate bars with their ingredients. These determine the overall taste and flavour of the chocolates, which consequently affect their ratings. The chocolate reviews are between 2006 and 2022. The dataset was last updated on June 26, 2022. ')


#INSPECTION
st.header('Inspection') 
st.markdown("""---""")
chocolate_df = pd.read_csv("Chocolate bar ratings 2022.csv")
# 1) Showing some Data
st.subheader('LET\'S LOOK AT THE DATA')
st.write(chocolate_df.head())
st.write('Here we are displaying a small portion of what our data looks like')
st.write("\n")
col1,col2 = st.columns(2)
# 3) Null values
col1.markdown('NULL VALUES')
col1.write(chocolate_df.isna().sum())
col1.write('Here we are displaying the number of null values for each feature')
# 4) Stat Values
col2.markdown('THE STATS')
col2.write(chocolate_df.describe())
col2.write('These are the statistical values of the current quantitative data')
st.write("\n")
st.subheader("Inspection Summary")
st.markdown("In inspection we learned, the min and max values of the quantatitive values, we learned about which possible features we should drop in our dataset, and we learned where our null values are. ")
st.markdown("""---""")


#CLEANING
st.header('Cleaning the Data')
#Removing all rows that contain null values
col1, col2 = st.columns(2)
col1.markdown('NULL VALUES BY COLUMN')
col1.write(chocolate_df.isna().sum())
chocolate_df.dropna(inplace=True)
chocolate_df.reset_index(drop=True, inplace=True)
col2.markdown('AFTER CLEANING')
col2.write(chocolate_df.isna().sum())
st.subheader("Reasoning:")
st.write("Dropped all rows with null values contained in them. This was necessary in order to keep a consistent dataset with the least amount of gaps. The number of missing values were low enough to not warrant any changes in columns, this is why the ingredients column was kept.")
st.markdown("""---""")
#Removing the REF Column
col1, col2 = st.columns(2)
column_to_drop = ['REF']
chocolate_df.drop(column_to_drop, axis = 1, inplace = True)
col1.markdown("DATA AFTER REMOVING THE REF COLUMN")
col1.write(chocolate_df.head(5))
col2.subheader("Reasoning:")
col2.write("Dropped the 'REF' column as it was not needed for the analysis and would serve no value to answering any of the hypotheses.")
st.markdown("")
#Turning the Cocoa % column into a float.
col1, col2 = st.columns(2)
chocolate_df['Cocoa Percent'] = chocolate_df['Cocoa Percent'].str.replace('%','').astype(float)
col1.markdown("COCOA % COLUMN CONVERTED TO FLOAT VALUES")
choc_subset = chocolate_df[['Cocoa Percent']]
col1.write(choc_subset.head())
col2.subheader("Reasoning:")
col2.write("Made the cocoa % column contain actual floats by taking out the '%' from the string. This was necessary because without taking out the percentage symbol, the column is read as a string and can not be used to perform the mathematical operations needed to analyze the data.")
st.markdown("")
#CONCLUSION
col1, col2 = st.columns(2)
col1.markdown("THE CLEANED STATS")
col1.write(chocolate_df.describe())
col2.subheader("Changes:")
col2.write("Notice the data count has decreased, the number summary is available for Cocoa Percent, and the REF column has been removed.")
st.markdown("""---""")
st.subheader("Cleaning Summary")
st.write("After inspecting, we decided that the REF Column needed to be dropped, rows containing null values should be dropped, and that the cocoa percent column contained values that needed to be converted into floats.")
st.markdown("""---""")
#END OF CLEANING

#Graphs(
#Graphs Code(
#H2
def rating(data):
    tempdf = data
    finaldf = pd.DataFrame()
    for i in tempdf['Rating'].unique().tolist():
        column = tempdf[tempdf['Rating'] == i]
        cocoamean = column["Cocoa Percent"].mean()
        data1 = {
            "Cocoa %": [cocoamean],
            "Rating": [i]
                }
        if cocoamean >=0:
            finaldf = pd.concat([finaldf,pd.DataFrame.from_records(data1)],ignore_index=True)
    return finaldf

table = rating(chocolate_df)
table = table.sort_values("Rating")
#H3
ratingsByYear = []
years = range(2006,2023)
for i in years:
    tempdf = chocolate_df[chocolate_df['Review Date']==i]
    ratingsByYear.append(tempdf['Rating'].mean())
data= list(zip(years,ratingsByYear))
myDF = pd.DataFrame(data, columns=['Year of Review','Average Rating'])
#H4
def rc(data):   
    ratingComp = pd.DataFrame()
    for i in data['Rating'].unique().tolist():
        column = data[data['Rating'] == i]
        column = column.groupby('Company (Manufacturer)')['Company (Manufacturer)'].count().sort_values(ascending = False)
        column = column[:2]
        t = {}
        t[i] = column
        ratingComp= pd.concat([ratingComp, pd.DataFrame.from_records([column])])
    return ratingComp

df_rc = rc(chocolate_df)
l = chocolate_df['Rating'].unique().tolist()
df_rc['Rating'] = l
#H5
def company_fav_ingredient(df):
    company_ing = pd.DataFrame()
    for i in df['Ingredients'].unique().tolist():

        column = df[df["Ingredients"] == i]

        column = column.groupby('Company (Manufacturer)')['Company (Manufacturer)'].count().sort_values(ascending=False)
        column = column[:3]
        #company_ing[i] = column.values
        t = {}
        t[i] = column
        company_ing = pd.concat([company_ing, pd.DataFrame.from_records([column])])
    return company_ing

df_cfi = company_fav_ingredient(chocolate_df)
l = chocolate_df['Ingredients'].unique().tolist()
df_cfi["Ingredients"] = l
#H6
df_temp = chocolate_df.copy()
df_temp['Country of Bean Origin']=df_temp['Country of Bean Origin'].astype('category').cat.codes
df_temp['Company Location']=df_temp['Company Location'].astype('category').cat.codes

df_temp.drop(['Company (Manufacturer)', 'Specific Bean Origin or Bar Name','Ingredients', 'Most Memorable Characteristics'], axis =1, inplace = True)

chocolate_df_corr = df_temp.corr() # Generate correlation matrix
x = list(chocolate_df_corr.columns)
y = list(chocolate_df_corr.index)
z = np.array(chocolate_df_corr)

figSix = ff.create_annotated_heatmap(
    z,
    x = x,
    y = y ,
    annotation_text = np.around(z, decimals=2),
    hoverinfo='z',
    colorscale='Brwnyl',
    showscale=True,
    )
figSix.update_xaxes(side="bottom")
figSix.update_layout(
    title_text='Correlation Heatmap', 
    title_x=0.5, 
    width=500, 
    height=500,
    yaxis_autorange='reversed',
    template='plotly_dark'
)
#)Graphs Interface(
st.header('The Organized Data')
st.subheader("HYPOTHESIS 1: What percentage of cocoa is most enjoyed?")
st.plotly_chart(px.pie(table, values= 'Rating',names = 'Cocoa %', title = 'Best Rated Cocoa Percent'))
st.markdown("- The ratings for different cocoa percentages varied from 1 to 4")
st.markdown("- Out of these ratings, the best ratings were distributed mostly with chocolates with the lowest cocoa Percentage")
st.markdown("- Between the top two Cocoa Percentages, there is a 0.8% difference in the distribution of best ratings, but there was a clear winner of 70.76%")
st.write("\n")
st.subheader("HYPOTHESIS 2: Is there an association between ratings and cocoa %?")
st.plotly_chart(px.line(table, x= 'Rating',y='Cocoa %', title = 'Cocoa Percentage by Chocolate Rating'))
st.markdown("- The highest average % of cocoa which was at 75.6% sat at a 1.5 rating while the lowest average % of cocoa which was 70.76% reached a full a 4.0 rating**")
st.markdown("- In comparison, the lowest rated chocolates which were at a 1.0 rating, had a 73% cocoa makeup on average")
st.markdown("- From a rating of 2.5 and onwards, the average % of cocoa used in chocolate maintained a value below 72%")
st.write("\n")
st.subheader("HYPOTHESIS 3: Does the date of review effect the rating of the chocolate bar?")
st.plotly_chart(px.line(myDF, x = 'Year of Review', y = 'Average Rating', template = 'plotly_dark', title = 'Average Rating by Year'))
st.markdown("- As the rating increases from 3.06 in 2006 to 3.28 in 2022, the correlation is positive")
st.markdown("- The percentage change between the start and end dates (2006-2022) is approximately 7%")
st.markdown("- The minimal amount of change demonstrated paired with the sporadic data leads towards the conclusion that DoR has minimal effect on the rating distributed")
st.write("\n")
st.subheader("HYPOTHESIS 4: What company consistently produces the best chocolate?")
st.plotly_chart(px.bar(df_rc, x = df_rc["Rating"], y = df_rc.columns.tolist(), template = 'plotly_dark', title = 'Ratings by Company', labels = {"value":"Quantity"}))
st.markdown("- We can consider the best chocolate to be ranked 3.25 or above")
st.markdown("- Based on the Bar Chart titled Ratings by Company, Soma is the only company that is consistent within the ratings of 3.25 - 4, making Soma the most consistent producer of the best chocolate")
st.write("\n")
st.subheader("HYPOTHESIS 5: Do the companies have a favorite ingredient combination, or are their recipes random?")
st.plotly_chart(px.bar(df_cfi, x = df_cfi["Ingredients"], y = df_cfi.columns.tolist(), title='Ingredients by Company', labels = {"value":"Quantity"}))
st.markdown("- Based on the bar graph, we can see that companies stick to 1-2 ingredient combinations, having a clear set of favorite ingredients")
st.markdown("- The ingredient combination (3-B, S, C) is the favorite of 3 companies: Soma, Fresco, and Bonnat")
st.markdown("- Their recipes are not random")
st.write("\n")
st.subheader("HYPOTHESIS 6: What is the correlation between different features of the data?")
st.plotly_chart(figSix)
st.markdown("- We can conclude that the features in our data is mostly of low correlation")
st.markdown("- The correlation stays in the low part of the range, some also having a negative correlation")

st.markdown("""---""")
#))End of Graphs

#Final Analysis of Graphs
st.header('Final Analysis of Hypotheses')
st.subheader('In total, we were able to answer 6 hypotheses:')
st.markdown("""---""")

st.subheader('*HYPOTHESIS 1: What percentage of cocoa is most enjoyed?*')
st.write('*The most enjoyed Cocoa % is 70.76%*')
st.markdown("""---""")

st.subheader('*HYPOTHESIS 2: Is there an association between ratings and cocoa %?*')
st.write('*On average, as the rating of the chocolate goes up, the percentage of cocoa used in the chocolate decreases*')
st.markdown("""---""")

st.subheader('*HYPOTHESIS 3: Does the date of review effect the rating of the chocolate bar?*')
st.write('*The relationship between YoR (Year of Review) and Rating is loosely proportional*')
st.markdown("""---""")

st.subheader('*HYPOTHESIS 4: What company consistently produces the best chocolate?*')
st.write("The most consistent producer of the best chocolate is Soma.")
st.markdown("""---""")

st.subheader('*HYPOTHESIS 5: Do the companies have a favorite ingredient combination, or are their recipes random?*')
st.write('*The companies tend to stick to one formula, or combination of ingredients*')
st.markdown("""---""")

st.subheader('*HYPOTHESIS 6: What is the correlation between different features of the data?*')
st.write('*Most of the correlations are relatively weak, ranging mostly under 0.04*')
st.markdown("""---""")








