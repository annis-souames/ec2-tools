from manage import (
    create_instance,
    list_regions,
    list_instances,
    delete_instance,
    get_status,
)
import typer

app = typer.Typer()


@app.command("list-regions")
def list_regions_command():
    """List all EC2 instances."""
    resp = list_regions()
    print("Regions:", resp["regions"])
    print("AZ list:", resp["zones"])


@app.command("list-instances")
def list_instances_command(region: str):
    """List all EC2 instances."""
    resp = list_instances(region)
    print(f"Found {len(resp)} instances in {region}:")
    for inst in resp:
        print(
            "-- IP =",
            inst["PrivateIpAddress"],
            "| Type:",
            inst["InstanceType"],
            "| ID:",
            inst["InstanceId"],
        )


@app.command("create")
def create_command(template_path: str, region: str):
    """Create a new EC2 instance."""
    id = create_instance(cfg_path=template_path, region=region)
    print(f"The instance {id} was created successfully.")


@app.command("delete")
def delete_command(instance_id: str, region: str):
    """Delete a specific EC2 instance."""
    delete_instance(instance_id=instance_id, region=region)
    print(f"Instance {instance_id} was deleted successfully.")


@app.command("status")
def status(instance_id: str, region: str):
    """Get status specific EC2 instance."""
    status = get_status(instance_id, region)
    print(f"Status of {instance_id}: {status}")


if __name__ == "__main__":
    app()
