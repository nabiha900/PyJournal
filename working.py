import sqlite3
import datetime
import streamlit as st

# Connect to SQLite database
connection = sqlite3.connect("pyjournal.db")
cursor = connection.cursor()

# Create journaling table if it doesn't exist
cursor.execute('''
create table if not exists journaling(
    id integer primary key autoincrement,
    date text,
    journal text
) ''')

# Set the title of the app
st.title("📘Welcome to Pyjournal")

# Sidebar header and separator
st.sidebar.markdown("# Pyjournal")
st.sidebar.markdown("---")

# Sidebar menu options for user to choose an action
choice = st.sidebar.selectbox("Choose an option:", ["Add New Memory", "View Memories", "Edit Memory", "Delete Memory"])

if choice == "Add New Memory":
    st.subheader("📌Add a New Memory:")
    memo = st.text_area("What's on your mind? ", height=150, max_chars=300, placeholder="Type your memory here...")
    
    # Save button - when clicked, save memory if not empty
    if st.button("Save Memory"):
        if memo.strip():  # Check that input is not just whitespace
            today = datetime.date.today()
            cursor.execute("insert into journaling(date,journal) values (?,?)", (today, memo))
            connection.commit()
            st.success("Memory added successfully!")
        else:
            st.warning("Please write something before saving")

elif choice == "View Memories":
    st.subheader("📖Previous Memories:")
    cursor.execute("select * from journaling")
    journaling = cursor.fetchall()
    
    if journaling:
        # Loop through all entries and display them formatted
        for j in journaling:
            st.markdown(f"""
                ---            
                **Memory ID**: {j[0]}      
                **Memory**: 
                > {j[2]} 

                **Date**: {j[1]}      
                """)
    else:
        st.info("No Memories Found")

elif choice == "Edit Memory":
    st.subheader("✏️Edit a Memory:")
    cursor.execute("select * from journaling")
    journaling = cursor.fetchall()
    
    if journaling:
        # Dropdown to select which memory to edit by ID
        id = st.selectbox("Select Memory ID To Edit:", [j[0] for j in journaling])
        cursor.execute("select journal from journaling where id = ?", (id,))
        selected = cursor.fetchone()
        
        # Text area pre-filled with the selected memory text
        new_memo = st.text_area("Edit memory: ", height=200, value=selected[0])
        
        # Update button to save changes
        if st.button("Update Memory"):
            if new_memo.strip():
                cursor.execute("update journaling set journal = ? where id = ?", (new_memo, id))
                connection.commit()
                st.success("Memory updated successfully!\n")
            else:
                st.warning("Updated memory can't be empty")
    else:
        st.info("No Memories available to edit")

elif choice == "Delete Memory":
    st.subheader("🗑️Delete a Memory:")
    
    # Fetch all memories to select which one to delete
    cursor.execute("select * from journaling")
    journaling = cursor.fetchall()
    
    if journaling:
        # Dropdown to select memory ID to delete
        id = st.selectbox("Select Memory ID To Delete:", [j[0] for j in journaling])
        
        # Delete button to remove the selected memory
        if st.button("Delete Memory"):
            cursor.execute("delete from journaling where id = ?", (id,))
            connection.commit()
            st.success("Memory deleted successfully")
    else:
        st.info("No memories available to delete")

# Close the database connection
connection.close()
