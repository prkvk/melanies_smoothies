# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie', max_chars= 10 )
st.write('The name on your Smoothie order will be:', name_on_order)

st.write(
   "Choose the fruits you want in your custom Smoothie!"
)

cnxs = st.connection("snowflake")
session1 = cnxs.session()

my_dataframe = session1.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose upto 5 ingredients:', my_dataframe, max_selections=5)



time_to_insert = st.button('Submit Order')



if ingredients_list:
    ingredients_string = ''
    st.write(ingredients_list)
    st.text(ingredients_list)
   
    for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
       st.subheader(fruit_chosen + ' Nutrition Information')
       fruits_response = requests.get("https://fruityvice.com/api/fruits")
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
       fruit_dataframe=st.dataframe(data=fruityvice_response.json(), use_container_width=True);
    st.write(fruits_response.json())

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + "','" + name_on_order + """')"""

    st.write(my_insert_stmt)
    if time_to_insert:

        session1.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!' , icon="✅")

#option = st.selectbox('What is your favourite fruit?', options=['Banana','Strawberries', 'Peaches'])
#st.write('You selected:', option);
