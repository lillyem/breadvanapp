import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.database import db, get_migrate
from App.models import User, Driver, Resident, Route, Stop



# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

# Bread Van App CLI Commands

# DRIVER COMMANDS 

driver_cli = AppGroup('driver', help='Driver commands')

@driver_cli.command("create") # flask driver create Alice Downtown    
@click.argument("name")
@click.argument("location_name")
def driver_create(name, location_name):
    if Driver.query.filter_by(driver_name=name).first():
        return click.echo(f"Driver '{name}' already exists.")
    d = Driver(driver_name=name, location_name=location_name)
    db.session.add(d); db.session.commit()
    click.echo(d.get_json())


@driver_cli.command("schedule") # flask driver schedule Alice Uptown 3
                                # 3 is the resident id

@click.argument("name")
@click.argument("location_name")
@click.argument("resident_id", type=int)  
def driver_schedule(name, location_name, resident_id):
    d = Driver.query.filter_by(driver_name=name).first_or_404()
    route = d.schedule_drive(location_name=location_name, resident_id=resident_id)  
    db.session.commit()
    click.echo(route.get_json())

@driver_cli.command("status") # flask driver status Alice
@click.argument("name")
def driver_status(name):
    d = Driver.query.filter_by(driver_name=name).first_or_404()
    click.echo(d.get_json())

@driver_cli.command("update-location") # flask driver update-location Alice Midtown
@click.argument("name")
@click.argument("location_name")
def driver_update_location(name, location_name):
    d = Driver.query.filter_by(driver_name=name).first_or_404()
    d.location_name = location_name
    db.session.commit()
    click.echo(f"{d.driver_name}'s location updated to {location_name}")

@driver_cli.command("update-status") #flask driver status Alice offline
@click.argument("name")
@click.argument("status")
def driver_update_status(name, status):
    d = Driver.query.filter_by(driver_name=name).first_or_404()
    d.status = status
    db.session.commit()
    click.echo(f"{d.driver_name}'s status updated to {status}")

app.cli.add_command(driver_cli)



# RESIDENT COMMANDS 

resident_cli = AppGroup('resident', help='Resident commands')

@resident_cli.command("create") # flask resident create Bob Uptown    
@click.argument("name")
@click.argument("location_name")
def resident_create(name, location_name):
    if Resident.query.filter_by(resident_name=name).first():
        return click.echo(f"Resident '{name}' already exists.")
    r = Resident(resident_name=name, location_name=location_name)
    db.session.add(r); db.session.commit()
    click.echo(r.get_json())

@resident_cli.command("inbox") # flask resident inbox Bob       
@click.argument("name")
def resident_inbox(name):
    r = Resident.query.filter_by(resident_name=name).first_or_404()
    routes = r.view_routes(r.location_name)
    click.echo([rt.get_json() for rt in routes] or f"No routes for {r.location_name}")

@resident_cli.command("request-stop") # flask resident request-stop Bob Alice
@click.argument("resident_name")
@click.argument("driver_name")
def resident_request(resident_name, driver_name):
    r = Resident.query.filter_by(resident_name=resident_name).first_or_404()
    d = Driver.query.filter_by(driver_name=driver_name).first_or_404()
    msg = r.send_request(d.driver_id, r.location_name)
    db.session.commit()
    click.echo(msg)

@resident_cli.command("track") # flask resident track Bob Alice        
@click.argument("resident_name")
@click.argument("driver_name")
def resident_track(resident_name, driver_name):
    r = Resident.query.filter_by(resident_name=resident_name).first_or_404()
    d = Driver.query.filter_by(driver_name=driver_name).first_or_404()
    click.echo(d.get_json())

app.cli.add_command(resident_cli)
