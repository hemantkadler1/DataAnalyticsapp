import pandas as pd 
import plotly.express as px 
import streamlit as st 

st.set_page_config(
    page_title='Consoleflare Analytics Portal', 
    page_icon='💻'
)
#title
st.title(':red[Data] :blue[Analytics] Portal',)
st.subheader(':gray[Explore Data with ease.]',divider='blue')

file=st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data=pd.read_csv(file)
    else:
        data=pd.read_excel(file)

    st.dataframe(data)
    st.info('File is successfully uploaded',icon="🚨")

    st.subheader(':blue[Basic] Information of the Dataset',divider='red')
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top and Bottom','Datatypes','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical Summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows =st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows =st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))
    with tab3:
        st.subheader(':gray[Data types of column]')
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader('column Name in Dataset')
        st.write(list(data.columns))

    st.subheader(':rainbow[columns values To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2=st.columns(2)
        with col1:
            column=st.selectbox('Choose Column name',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top rows',min_value=1,step=1)

        count=st.button('Count')
        if(count==True):
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualisation',divider='gray')
            fig=px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig=px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig=px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Group By: Simplify Your Data Analysis]',divider='red')
    st.write("The 'Group By' option lets you organize and summarize your data.") 
    with st.expander('Groupby Operations'):
    
        col1, col2, col3 = st.columns(3)

    with col1:
        groupby_cols = st.multiselect('Choose columns to group by',options=list(data.columns))

    with col2:
        operation_col = st.selectbox('Choose Column for operation',options=list( data.columns))

    with col3:
        operation = st.selectbox('Choose Operation', options=['sum', 'mean', 'max', 'min','median','count'])

    # Perform Group By if selections are made
    if (groupby_cols):
            result = data.groupby(groupby_cols).agg(newcol=(operation_col,operation)).reset_index()
            st.dataframe(result)       
           
           

            st.subheader("Gray Data Visualization", divider="gray")

            graphs = st.selectbox("Choose your graph", options=["line", "bar", "scatter", "pie", "sunburst"])

            if graphs == "line":
                x_axis = st.selectbox("Choose X axis", options=list(result.columns))
                y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None] + list(result.columns))
                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers=True)
                st.plotly_chart(fig)

            elif graphs == "bar":
                x_axis = st.selectbox("Choose X axis", options=list(result.columns))
                y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None] + list(result.columns))
                facet_col = st.selectbox("Column Information", options=[None] + list(result.columns))

                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col)
                st.plotly_chart(fig)

            elif graphs == "scatter":
                x_axis = st.selectbox("Choose X axis", options=list(result.columns))
                y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None] + list(result.columns))
                size = st.selectbox("Size Column", options=[None] + list(result.columns))

                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)

            elif graphs == "pie":
                names = st.selectbox("Choose labels", options=list(result.columns))
                values = st.selectbox("Choose Numerical Values", options=list(result.columns))

                fig = px.pie(data_frame=result, values=values, names=names)
                st.plotly_chart(fig)

            elif graphs == "sunburst":
                path = st.multiselect("Choose your Path", options=list(result.columns))
                values = st.selectbox("Choose Numerical Values", options=list(result.columns))

                fig = px.sunburst(data_frame=result, path=path, values=values)
                st.plotly_chart(fig)
