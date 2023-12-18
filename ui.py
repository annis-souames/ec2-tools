import streamlit as st
import config
from manage import (
    create_instance,
    delete_instance,
    list_instances,
    get_status,
    list_regions,
)


# Streamlit UI
def main():
    st.title("EC2 Instance Manager")

    st.sidebar.header("Menu")
    menu_options = [
        "List Instances",
        "Create Instance",
        "Delete Instance",
        "Instance Status",
    ]
    selected_option = st.sidebar.selectbox("Select an option", menu_options)

    if selected_option == "List Instances":
        list_instances_ui()
    elif selected_option == "Create Instance":
        create_instance_ui()
    elif selected_option == "Delete Instance":
        delete_instance_ui()
    elif selected_option == "Instance Status":
        instance_status_ui()


# UI for listing instances
def list_instances_ui():
    st.header("List EC2 Instances")

    region = st.selectbox("Select Region", get_regions())
    instances = list_instances(region)

    if instances:
        st.table(instances)
    else:
        st.info("No instances found in the selected region.")


# UI for creating an instance
def create_instance_ui():
    st.header("Create EC2 Instance")

    region = st.selectbox("Select Region", get_regions())
    st.info(
        "Make sure to provide valid AMI ID, instance type, and volume size in the 'config.py' file."
    )

    if st.button("Create Instance"):
        create_instance(region)
        st.success(
            "EC2 instance creation initiated. Check your AWS Console for status."
        )


# UI for deleting an instance
def delete_instance_ui():
    st.header("Delete EC2 Instance")

    region = st.selectbox("Select Region", get_regions())
    instance_id = st.text_input("Enter Instance ID")

    if st.button("Delete Instance"):
        if instance_id:
            delete_instance(instance_id, region)
            st.success(
                f"Initiated termination for EC2 instance {instance_id}. Check your AWS Console for status."
            )
        else:
            st.warning("Please enter a valid Instance ID.")


# UI for getting the status of an instance
def instance_status_ui():
    st.header("Check EC2 Instance Status")

    region = st.selectbox("Select Region", get_regions())
    instance_id = st.text_input("Enter Instance ID")

    if st.button("Get Status"):
        if instance_id:
            status = get_status(instance_id, region)
            st.success(f"The status of EC2 instance {instance_id} is: {status}")
        else:
            st.warning("Please enter a valid Instance ID.")


def get_regions():
    regions_data = list_regions()
    regions = [region["RegionName"] for region in regions_data["regions"]]
    return regions


if __name__ == "__main__":
    main()
