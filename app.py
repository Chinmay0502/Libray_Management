import streamlit as st
from library_backend import Library

st.set_page_config(page_title="Library Management", layout="wide")

st.title("📚 Library Management System")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Book",
        "View Books",
        "Add Member",
        "View Members",
        "Borrow Book",
        "Return Book"
    ]
)


# ---------------------------------
if menu == "Add Book":
    st.subheader("Add New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    copies = st.number_input("Number of Copies", min_value=1, step=1)

    if st.button("Add Book"):
        Library.add_book(title, author, copies)
        st.success("Book Added Successfully!")

# ---------------------------------
elif menu == "View Books":
    st.subheader("Available Books")

    books = Library.get_books()

    if books:
        st.dataframe(books)
    else:
        st.warning("No Books Found")

# ---------------------------------
elif menu == "Add Member":
    st.subheader("Add New Member")

    name = st.text_input("Member Name")
    email = st.text_input("Email")

    if st.button("Add Member"):
        Library.add_member(name, email)
        st.success("Member Added Successfully!")

# ---------------------------------
elif menu == "View Members":
    st.subheader("Registered Members")

    members = Library.get_members()

    if members:
        st.dataframe(members)
    else:
        st.warning("No Members Found")

elif menu == "Borrow Book":
    st.subheader("Borrow Book")

    members = Library.get_members()
    books = Library.get_books()

    if not members or not books:
        st.warning("Members or Books missing")
    else:
        member_ids = [m["id"] for m in members]
        book_ids = [b["id"] for b in books]

        selected_member = st.selectbox("Select Member ID", member_ids)
        selected_book = st.selectbox("Select Book ID", book_ids)

        if st.button("Borrow"):
            result = Library.borrow_book(selected_member, selected_book)
            if "successfully" in result:
                st.success(result)
            else:
                st.error(result)

elif menu == "Return Book":
    st.subheader("Return Book")

    members = Library.get_members()

    if not members:
        st.warning("No members found")
    else:
        member_ids = [m["id"] for m in members]
        selected_member = st.selectbox("Select Member ID", member_ids)

        member = next(m for m in members if m["id"] == selected_member)

        if not member["borrowed"]:
            st.info("This member has no borrowed books")
        else:
            borrowed_books = [b["book_id"] for b in member["borrowed"]]
            selected_book = st.selectbox("Select Book to Return", borrowed_books)

            if st.button("Return Book"):
                result = Library.return_book(selected_member, selected_book)
                if "successfully" in result:
                    st.success(result)
                else:
                    st.error(result)

