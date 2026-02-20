import streamlit as st 
import json
import pandas as pd
from datetime import datetime
from main import add_property, add_guest, view_properties, view_guests, add_booking, view_bookings
from reports import total_income, bookings_per_property, monthly_income

st.title("🏠 Airbnb Manager Dashboard")

menu = st.sidebar.selectbox("Menu:", ["Properties", "Guests", "Bookings", "Reports"])

if menu == "Properties":
    properties = view_properties()
    if properties:
        df = pd.DataFrame(properties)
        st.dataframe(df)
    else:
        st.info("هیچ property ای نیست.")

    with st.form("add_property"):
        st.subheader("➕ Add Property")
        name = st.text_input("Name")
        address = st.text_input("Address")
        rooms = st.number_input("Number of Room", min_value=1, step=1)
        price = st.number_input("Price Per Night ($)", min_value=0.0, step=10.0)
        amenities_input = st.text_input("Amentites (e.g.: wifi, pool)split with ','")
        status = st.selectbox("وضعیت", ["available", "booked"])
        if st.form_submit_button("ذخیره"):
            from properties import create_property
            from storage import load_properties, save_properties
            amenities = [a.strip() for a in amenities_input.split(",") if a.strip()]
            new_p = create_property(name, address, int(rooms), float(price), amenities, status)
            all_props = load_properties()
            all_props.append(new_p)
            save_properties(all_props)
            st.success("Property Added!")
            st.rerun()


elif menu == "Guests":
    guests = view_guests()
    if guests:
        df = pd.DataFrame(guests)
        st.dataframe(df)
    else:
        st.info("There is no guest!")
    
    with st.form("add_guest"):
        st.subheader("Add Guest")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        if st.form_submit_button("Save"):
            from guests import create_guest
            from storage import load_guests, save_guests
            new_g = create_guest(name, int(phone), email)
            all_guests = load_guests()
            all_guests.append(new_g)
            save_guests(all_guests)
            st.success("Guest added!")
            st.rerun()

elif menu == "Bookings":
    bookings = view_bookings()
    if bookings:
        df = pd.DataFrame(bookings)
        st.dataframe(df)
    else:
        st.info("هیچ رزروی نیست.")

    props = view_properties()
    guests = view_guests()

    if props and guests:
        with st.form("add_booking"):
            st.subheader("➕ Add Booking")
            prop_names = [p["name"] for p in props]
            guest_names = [g["name"] for g in guests]
            sel_prop = st.selectbox("Property", prop_names)
            sel_guest = st.selectbox("Guest", guest_names)
            start = st.date_input("تاریخ شروع")
            end = st.date_input("تاریخ پایان")
            if st.form_submit_button("رزرو کن"):
                from storage import load_bookings, save_bookings
                from bookings import create_booking
                from validators import has_conflict
                prop_idx = prop_names.index(sel_prop)
                guest_idx = guest_names.index(sel_guest)
                start_str = start.strftime("%Y-%m-%d")
                end_str = end.strftime("%Y-%m-%d")
                all_bookings = load_bookings()
                if has_conflict(start_str, end_str, all_bookings, prop_idx + 1):
                    st.error("این property در این تاریخ رزرو است!")
                else:
                    nights = (end - start).days
                    if nights <= 0:
                        st.error("تاریخ پایان باید بعد از شروع باشد!")
                    else:
                        total = nights * props[prop_idx]["price_per_night"]
                        b = create_booking(prop_idx+1, guest_idx+1, start_str, end_str, total)
                        all_bookings.append(b)
                        save_bookings(all_bookings)
                        st.success(f"رزرو شد! {nights} شب — ${total:.2f}")
                        st.rerun()
    else:
        st.warning("اول property و guest اضافه کن.")


elif menu == "Reports":
    from reports import total_income, bookings_per_property, monthly_income
    from storage import load_bookings, load_properties
    bookings = view_bookings()
    props = view_properties()

    if not bookings:
        st.warning("هنوز رزروی ثبت نشده.")
    else:
        st.metric("💰 درآمد کل", f"${total_income(bookings):.2f}")

        st.subheader("📊 رزرو هر ملک")
        counts = bookings_per_property(bookings, props)
        df_counts = pd.DataFrame([{"Property": k, "Bookings": v} for k, v in counts.items()])
        st.bar_chart(df_counts.set_index("Property"))

        st.subheader("📅 درآمد ماهانه")
        monthly = monthly_income(bookings)
        df_monthly = pd.DataFrame([{"Month": k, "Income": v} for k, v in sorted(monthly.items())])
        st.line_chart(df_monthly.set_index("Month"))
